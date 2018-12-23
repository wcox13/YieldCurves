import csv
import requests
import xml.etree.ElementTree as ElementTree

tolerance = .25

xml_file = 'yields.xml'
csv_file = 'yields.csv'

headers = [
    'DATE',
    #'1MONTH',
    #'2MONTH',
    '3MONTH',
    '6MONTH',
    '1YEAR',
    '2YEAR',
    '3YEAR',
    '5YEAR',
    #'7YEAR',
    '10YEAR',
    #'20YEAR',
    #'30YEAR',
]

maturities = headers[1:] # i.e. everything except 'Date'

def strip_prefix(string):
    return string.split('}')[1]

def get_tag(node):
    return strip_prefix(node.tag)

def parse_date(datestring):
    return datestring.split('T')[0]

def parse_maturity(maturity):
    return maturity.split('_')[1] if '_' in maturity else None

def parse_yield(yield_val):
    return float(yield_val) if yield_val else None

def loadRSS():

    # url of rss feed
    url = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData'

    # creating HTTP response object from given url
    response = requests.get(url)

    # saving the xml file
    with open(xml_file, 'wb') as f:
        f.write(response.content)


def parseXML(xmlfile):

    yield_curves = []

    # create element tree object
    tree = ElementTree.parse(xmlfile)

    root = tree.getroot()
    for entry in root:

        # ignore the initial header stuff
        if get_tag(entry) != 'entry':
            continue

        # handle totally unnecessary nesting
        content = entry[6]
        properties = content[0]

        yield_curve = {}

        # add date
        date = parse_date(properties[1].text)
        yield_curve['DATE'] = date

        # only include 1st of each month
        if date.endswith('01'):

            # parse yield curve
            for yield_entry in properties:

                tag = strip_prefix(yield_entry.tag)
                maturity = parse_maturity(tag)

                if maturity in maturities:
                    yield_val = parse_yield(yield_entry.text)
                    yield_curve[maturity] = float(yield_val)

            # only add curves with an inversion
            if hasInversion(yield_curve):
                yield_curves.append(yield_curve)

    return sorted(yield_curves, key=lambda curve: curve['DATE'])

def hasInversion(yield_curve):
    num_maturities = len(maturities)
    for i in range(num_maturities):
        for j in range(i, num_maturities):
            if yield_curve[maturities[i]] > yield_curve[maturities[j]] + tolerance:
                return True
    return False

def savetoCSV(yield_curves, filename):

    # writing to csv file
    with open(filename, 'w') as csvfile:

        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = headers)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(yield_curves)


def main():
    # load rss from web to update existing xml file
    loadRSS()

    # parse xml file
    newsitems = parseXML(xml_file)

    # store news items in a csv file
    savetoCSV(newsitems, csv_file)


if __name__ == "__main__":

    # calling main function
    main()
