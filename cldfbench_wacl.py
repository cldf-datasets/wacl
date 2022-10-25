import pathlib
import subprocess
import collections

from pycldf import Sources
from cldfbench import Dataset as BaseDataset, CLDFSpec
from clldutils.misc import slug
from clldutils.text import split_text


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "wacl"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module='StructureDataset')

    def cmd_download(self, args):
        pass

    def cmd_readme(self, args):
        subprocess.check_call([
            'cldfbench',
            'cldfviz.map',
            str(self.cldf_specs().metadata_path),
            '--parameters', 'CLF',
            '--output', str(self.dir / 'map.jpg'),
            '--width', '20',
            '--height', '10',
            '--format', 'jpg',
            '--pacific-centered'])
        desc = [
            '\n{}'.format(self.cldf_reader().properties['dc:description']),
            '\n![Distribution of classifier languages](map.jpg)\n'
        ]
        pre, head, post = super().cmd_readme(args).partition('## CLDF ')
        return pre + '\n'.join(desc) + head + post

    def cmd_makecldf(self, args):
        values = list(self.raw_dir.read_csv('WACL_v1.csv', delimiter=',', dicts=True))
        args.writer.cldf.properties['dc:description'] = \
            "The database, named World Atlas of Classifier Languages (WACL), has been " \
            "systematically constructed over the last ten years via a manual survey of relevant " \
            "literature and also an automatic scan of digitized grammars followed by manual " \
            "checking. WACL presents a precise definition of numeral classifiers, steps to " \
            "identify a numeral classifier language, and a database of {} languages, of which " \
            "{} languages have been identified as having a numeral classifier system. " \
            "The open-access release of WACL is thus a significant contribution to linguistic " \
            "research in providing (i) a precise definition and examples of how to identify " \
            "numeral classifiers in language data and (ii) the largest dataset of numeral " \
            "classifier languages in the world. As such it offers researchers a rich and stable " \
            "data source for conducting typological, quantitative, and phylogenetic analyses on " \
            "numeral classifiers. The database will also be expanded with additional features " \
            "relating to numeral classifiers in the future in order to allow more fine-grained " \
            "analyses.".format(len(values), sum(1 for r in values if r['CLF'] == 'TRUE'))
        args.writer.cldf.add_component('ParameterTable')
        args.writer.cldf.add_component(
            'LanguageTable',
            'Continent',  # we add more language metadata
        )
        args.writer.cldf['LanguageTable', 'Latitude'].null = ['', 'NA']
        args.writer.cldf['LanguageTable', 'Longitude'].null = ['', 'NA']
        args.writer.cldf['LanguageTable', 'ISO639P3code'].null = ['', 'NA']
        args.writer.cldf.add_component('CodeTable')

        args.writer.objects['ParameterTable'] = [
        {
            'ID': 'CLF',
            'Name': 'CLF',
            'Description':
            'Does the language have sortal classifiers, regardless of optional of obligatory?'
        }]
        args.writer.objects['CodeTable'] = [
            {'ID': 'CLF-1', 'Parameter_ID': 'CLF', 'Name': 'TRUE'},
            {'ID': 'CLF-0', 'Parameter_ID': 'CLF', 'Name': 'FALSE'},
        ]
        codes = {r['Name']: r['ID'] for r in args.writer.objects['CodeTable']}

        l2s = collections.defaultdict(list)
        sources = []
        for src in sorted(
                Sources.from_file(self.raw_dir / 'sources.bib').items(), key=lambda i: i.id):
            for k in ['title', 'author', 'editor']:
                if k in src:
                    src[k] = src[k].replace('{', '').replace('}', '')
            if src.get('glottocode'):
                for code in split_text(src['glottocode'], ';', strip=True):
                    l2s[code].append(src.id)
                sources += [src]

        args.writer.cldf.add_sources(*sources)

        for row in self.raw_dir.read_csv('WACL_v1.csv', delimiter=',', dicts=True):
            lidx = slug(row['glottocode'], lowercase=False)
            args.writer.objects['LanguageTable'].append({
                'ID': lidx,
                'Glottocode': row['glottocode'],
                'Name': row['language_name'],
                'Latitude': row['latitude'],
                'Longitude': row['longitude'],
                'ISO639P3code': row['iso_code'],
                'Continent': row['continent']
            })
            for param in ['CLF']:
                args.writer.objects['ValueTable'].append({
                    "ID": '{}-CLF'.format(lidx),
                    "Value": row[param],
                    "Language_ID": lidx,
                    "Parameter_ID": 'CLF',
                    "Code_ID": codes[row[param]],
                    "Source": l2s.get(row['glottocode'], [])
                })
