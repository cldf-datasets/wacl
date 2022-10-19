import pathlib
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

    def cmd_makecldf(self, args):
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
