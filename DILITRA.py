'''
Script principal
'''

from plscadd_report import pls_summary
from atp_xml import xml_file

def main():

    xml_file(pls_summary=pls_summary)

if __name__ == '__main__':
    main()
