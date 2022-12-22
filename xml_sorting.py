from logging import root
import re
import xml.etree.ElementTree as ET
import collections
import io
#part form pytest
import os

# Get the current working directory
cwd = os.getcwd()

# Change the working directory to the location of the script file
os.chdir(os.path.dirname(__file__))

# Do something with the working directory
print(os.getcwd())

xml_string = ET.parse('etalon.xml')
xml_string2 = ET.parse('compare.xml')

tree_orig = xml_string.getroot()

tree_test = xml_string2.getroot()

parent_of_element = 'Transactions'
element_to_order = "Transaction"
order_by = 'Arn'

# find Arn and compare of two files:
#1. Check length of files:
if len(tree_orig.findall('.//*')) == len(tree_test.findall('.//*')):
	print('Length of file is OK')
	#2. Check amount of Transaction in file:
	if len(tree_orig.findall('.//' + element_to_order)) == len(tree_test.findall('.//'+element_to_order)):
		print('Length of file is OK')
		correct_order = list(map(lambda a: a.text,tree_orig.findall('.//'+order_by)))
		#3. Check order of Arn 
		#list - create a list, map - function for each in list, soreted - works fine with key function
		if (list(map(lambda a: a.text, sorted(tree_orig.findall('.//'+order_by), key = lambda arn: arn.text))) ==
			list(map(lambda a: a.text, sorted(tree_test.findall('.//'+order_by), key = lambda arn: arn.text)))) :
			sorted_transaction_list = []
			for sorted_transaction in list(map(lambda a: a.text, tree_orig.findall('.//'+order_by))):
				for transaction in tree_test.findall('.//'+element_to_order):
					if (transaction.find('.//'+order_by).text == sorted_transaction):
						sorted_transaction_list.append(transaction)
						break		
			print('Order of Arn is correct')
			i = 0
			for transaction in tree_test.findall('.//'+element_to_order):
				tree_test.find('.//'+parent_of_element).remove(transaction)
				tree_test.find('.//'+parent_of_element).append(sorted_transaction_list[i])
				i=i+1

			replace_file = ET.tostring(tree_test, encoding="utf-8", xml_declaration=True).decode()
	
			with open('test.xml', 'w') as f:
				f.write(replace_file)
		else:
			print('Order either Arn does not match')
	else: 
		print('Length of file is different!')
else: 
    print('Length of file is different!')

























transaction_orig = []
transaction_test = []

for node in tree_orig.iter('Transaction'):    
    transaction_orig.append(node.find("Arn").text)


for node in tree_test.iter('Transaction'):
    transaction_test.append(node.find("Arn").text)
    # print(node.iter("Arn").text)    
    
# print(transaction_orig)
# print(transaction_test)

   
    # for elem in node.iter():
    #     if elem.tag == node.tag:
    #         print("{}: {}".format(elem.tag, elem.text))