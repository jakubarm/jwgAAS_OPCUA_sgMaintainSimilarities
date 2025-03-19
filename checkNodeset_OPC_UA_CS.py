import os
import xml.etree.ElementTree as ET

SEARCHED_UA_ELEMENTS = ["UAObject", "UAVariable"]

def get_xml_files(directory):
    """ Traverse the directory and return a list of XML files. """
    xml_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".NodeSet2.xml"):
                xml_files.append(os.path.join(root, file))
    return xml_files

def parse_elements(xml_file):
    """ Parse the XML file and extract UA elements (UAObject, UAVariable) with displayName and description. """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        uaelements_info = []

        ns = {'ua': 'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd'}

        # Iterate through all UA elements
        for searched_ua_element in SEARCHED_UA_ELEMENTS:
            for uaelement in root.findall('.//ua:' + searched_ua_element, ns):
                uaelement_info = {"file": xml_file, "uaElement": uaelement.tag}

                # Find displayName and description sub-elements
                display_name = uaelement.find("ua:DisplayName", ns)
                description = uaelement.find("ua:Description", ns)

                if display_name is not None:
                    uaelement_info['displayName'] = display_name.text
                if description is not None:
                    uaelement_info['description'] = description.text

                uaelements_info.append(uaelement_info)

        return uaelements_info
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
        return []

def main(directory):
    # Step 1: Get all XML files in the directory
    xml_files = get_xml_files(directory)
    all_uaelements = []

    # Step 2: Process each XML file
    for xml_file in xml_files:
        uaelements = parse_elements(xml_file)
        all_uaelements.extend(uaelements)

    # Step 3: Output the results
    if all_uaelements:
        for item in all_uaelements:
            print(f"File: {item['file']}")
            print(f"  UA element: {item['uaElement']}")
            if 'displayName' in item:
                print(f"    displayName: {item['displayName']}")
            if 'description' in item:
                print(f"    description: {item['description']}")
            print()
    else:
        print("No UA elements found in the XML files.")

if __name__ == "__main__":
    #directory = input("Enter the directory path of the nodeset: ")
    directory = 'E:/PROJECTS/UA-Nodeset/PADIM'
    main(directory)
