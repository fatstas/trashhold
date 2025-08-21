import xml.etree.ElementTree as ET


def parse_table(filepath, sheet_name=None, filtrated_report=False, lines=True, commonlines=True):
    probes = {}
    table = {}
    xml = ET.parse(filepath)
    for probe in xml.find('probes').findall('probe'):
        id = probe.get('id')
        name = probe.get('name')
        probes[id] = {'name': name, 'is_parallel': False}
        table[name] = {}
        for spe in probe.findall('spe'):
            parallel_name = spe.get('name')
            parallel_id = spe.get('id')
            probes[parallel_id] = {'name': name, 'parallel_name': parallel_name, 'is_parallel': True}

    for sheet in xml.find('columns').findall('sheet'):
        if sheet_name and sheet_name != sheet.get('name'):
            continue

        for column in sheet.findall('column'):
            type = column.get('type')
            report = column.get('report')

            if filtrated_report and report == 'no':
                continue

            if type == 'line':
                element = column.find('element').text
                wl = float(column.find('wl').text)
                wl = (wl, column.get('name'))
                if not lines:
                    continue

            elif type == 'commonLine':
                element = column.find('element').text
                wl = ('common', sheet.get('name'))
                if not commonlines:
                    continue

            else:
                continue

            for cell in column.find('cells').findall('pc'):
                sample_id = cell.get('i')
                attested_value = cell.get('cm')
                found_value = cell.get('v')
                sample_name = probes[sample_id]['name']
                table[sample_name].setdefault(element, {'intensitys': {}, 'found_value': {}})
                table[sample_name][element]['attested_value'] = attested_value
                table[sample_name][element]['found_value'][wl] = found_value

                for parallel in cell.findall('cl'):
                    try:
                        value = float(parallel.find('c').get('v'))
                        table[sample_name][element]['intensitys'].setdefault(wl, []).append(value)
                    except AttributeError:
                        pass

    return table


def parser_mnd(path):
    elements = {}
    metadata = {}
    default_meta = {}

    with open(path, 'r') as file:

        for line in file:
            if len(line) == 1 or 'Version' in line:
                continue

            elif line[0] in '0123456789':
                number, symbol, element, *other = line.split('    ')
                elements[symbol] = {'number': number, 'element': element, 'lines': {}}
                continue

            elif line[0] == ' ':
                wl, *meta = line.split()
                wl = float(wl)
                elements[symbol]['lines'].setdefault(wl, default_meta.copy())
                for f in meta:
                    if '=' in f:
                        index, value = f.split('=')
                        elements[symbol]['lines'][wl][index] = float(value)

                    elif '/' in f:
                        for letter in f[1:]:
                            elements[symbol]['lines'][wl][f'/{letter}'] = True

            elif line[0] == '#':
                continue

            else:
                flag, flag_name, *other = line.split('=')
                if '/' in flag:
                    its_flag = True
                    default_meta[flag] = False
                else:
                    its_flag = False
                    default_meta[flag] = None
                metadata[flag] = [flag_name, its_flag]
                continue

    for element in elements:
        elements[element]['number_lines'] = len(elements[element]['lines'])

    return elements


def parse_concentration(link):
    with open(link, 'r') as file:
        rm = {}
        _elements = {}
        elements, *file = file
        elements = elements.split('\t')
        for index, element in enumerate(elements[1:]):
            _elements[index] = element
        for sample in file:
            name, *concentrations = sample.split('\t')
            rm[name] = {}
            for i, value in enumerate(concentrations[:-1]):
                if len(value) != 0:
                    rm[name][_elements[i]] = float(value.replace(',', '.'))
                else:
                    rm[name][_elements[i]] = None

    return rm
