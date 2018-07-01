#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   R. Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

pmt_info = {}
pmt_info['db_name'] = 'buav'
pmt_info['domain_name'] = 'www.linuxden.com'
pmt_info['browser_username'] = 'usrbuv'
pmt_info['browser_password'] = 'usr1buv'
pmt_info['help_file'] = 'help.html'

def table_privileges():
    privileges = { \
	'project_info' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'pai' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'task' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'spr' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'ecp' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'project_members' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'priviledges' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    }, \
	'action_item_types' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'dispositions' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'ecp_prefixes' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'ecp_types' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'ecp_statuses' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'member_roles' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'spr_categories' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'signature_functions' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'problem_duplications' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'spr_prefixes' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'spr_priorities' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'spr_statuses' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	'us_states' : { \
	    pmt_info['browser_username'] : ['SELECT','INSERT','UPDATE','DELETE'] \
	    },
	}

    return privileges

def define_tables():
    data_tables = { \
	'project_info' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'Project Id', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : '1', \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your project id')" \
		}, \
	    'name': { \
		'label' : 'Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.name',"'Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Project Name')" \
		}, \
	    'address_line_1' : { \
		'label' : 'Address Line 1', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Address Line 1')" \
		}, \
	    'address_line_2' : { \
		'label' : 'Address Line 2', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Address Line 2')" \
		}, \
	    'city' : { \
		'label' : 'City', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
	    'state' : { \
		'label' : 'State', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM us_states ORDER BY state_abbreviation" \
		}, \
	    'zip' : { \
		'label' : 'Zip Code', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the zip code')" \
		}, \
	    'email' : { \
		'label' : 'E-mail Address', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'display_link' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the e-mail address')" \
		}, \
	    'phone_number_voice' : { \
		'label' : 'Phone Number (Voice)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_voice","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the phone number (Voice)')", \
		'format' : "###-###-####" \
		}, \
	    'phone_number_fax' : { \
		'label' : 'Phone Number (FAX)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_fax","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the phone number (FAX)')", \
		'format' : "###-###-####" \
		}}, \
	'inventory' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'Inventory Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Inventory Id')" \
		}, \
	     'po_id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'PO Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Item Id')" \
		}, \
	     'po_number' : { \
		'label' : 'PO Number', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Number')" \
		}, \
	     'project_id' : { \
		'label' : 'Project ID', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.project_id', "'Project ID'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Project ID')" \
		}, \
             'line_item' : { \
		'label' : 'Line Item ID', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.line_item', "'Line Item'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Line Item ID')", \
		'lov': "SELECT line_item FROM po_line_item ORDER BY line_item" \
		}, \
             'quantity' : { \
		'label' : 'Quantity', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.quantity', "'Quantity'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Quantity')" \
		}, \
             'description' : { \
		'label' : 'Description', \
		'type': 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.description', "'Description'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Description')" \
		}, \
             'unit_price' : { \
		'label' : 'Unit Price', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.unit_price', "'Unit Price'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Unit Price')" \
		}, \
             'total_unit_price' : { \
		'label' : 'Total Unit Price', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.total_unit_price', "'Total Unit Price'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Total Unit Price')" \
		}, \
             #'subtotal' : { \
		#'label' : 'Subtotal', \
		#'type': 'VARCHAR', \
		#'db_size' : '12', \
		#'form_size' : '12', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 10, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.subtotal', "'Subtotal'"], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Subtotal')" \
		#}, \
             #'shipping_handling' : { \
		#'label' : 'Shipping/Handling', \
		#'type': 'VARCHAR', \
		#'db_size' : '12', \
		#'form_size' : '12', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 11, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.shipping_handling', "'Shipping/Handling'"], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Shipping/Handling')" \
		#}, \
             #'tax_exempt' : { \
		#'label' : 'Tax Exempt', \
		#'type': 'VARCHAR', \
		#'db_size' : '12', \
		#'form_size' : '12', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 12, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.tax_exempt', "'Tax Exempt'"], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Tax Exempt')" \
		#}, \
             #'po_total' : { \
		#'label' : 'PO Total', \
		#'type': 'VARCHAR', \
		#'db_size' : '12', \
		#'form_size' : '12', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 13, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.po_total', "'PO Total'"], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('PO Total')" \
		#}, \
             #'quote_number' : { \
		#'label' : 'Quote Number', \
		#'type': 'VARCHAR', \
		#'db_size' : '12', \
		#'form_size' : '12', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 14, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.quote_number', "'Quote Number'"], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Quote Number')" \
		#}, \
	    'property_id_number' : { \
		'label' : 'Property ID #', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' :['form.property_id_number', 20, "'Property ID #'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Property ID #')" \
		}, \
             'prop_id_assigned_by_username' : { \
		'label' : 'Property ID# Assigned By Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Property ID# Assigned By Username')" \
		}, \
             'prop_id_assigned_by_password' : { \
		'label' : 'Property ID# Assigned By Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type': 'password', \
		'value' : '', \
		'display_order' : 17, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Property ID# Assigned By Password')" \
		}, \
             'prop_id_assigned_by_signature' : { \
		'label' : 'Property ID# Assigned By Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 18, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Property ID# Assigned By Signature')" \
		}, \
            'prop_id_assigned_by_sig_func' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
             'date_property_id_assigned' : { \
		'label' : 'Date Property ID# Assigned ', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 20, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.date_property_id_assigned", "'Date Property ID# Assigned'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Date Property ID# Assigned')", \
		'format' : "MM-DD-YYYY" \
		}, \
             'property_location' : { \
		'label' : 'Property Location', \
		'type': 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 21, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.property_location', 50, "'Property Location'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Property Location')" \
		}, \
	    'serial_number' : { \
		'label' : 'Serial Number', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 22, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.serial_number', 20, "'Serial Number'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Serial Number')" \
		}, \
	    'part_number' : { \
		'label' : 'Part Number', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 23, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.part_number', 20, "'Part Number'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Part Number')" \
		}, \
 	    'category' : { \
		'label' : 'Category', \
		'type': 'VARCHAR', \
		'db_size' : '22', \
		'form_size' : '22', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 24, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Category')", \
		'lov' : "SELECT category  FROM categories ORDER BY category" \
		}}, \
	'po' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'PO Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Item Id')" \
		}, \
	    'po_gist' : { \
		'label' : 'PO Gist', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.po_gist', "'PO Gist'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Gist')" \
		}, \
	    'po_number' : { \
		'label' : 'PO Number', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Number')" \
		}, \
	    'revision_number' : { \
		'label' : 'Revision Number', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Revision Number')" \
		}, \
	    'billing_address' : { \
		'label' : 'Billing Address', \
		'type': 'VARCHAR', \
		'db_size' : '500', \
		'form_size' : '500', \
		'default' : "Institute for Scientific Research, Inc.\nP. O. Box 1148\nFairmont, WV 26555-1148\nPhone: (304)368-9300\nFax:   (304)368-9313", \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
		'validation_routine': 'checkLength', \
		'validation_arguments': ['form.billing_address', 500, "'Billing Address'", 1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Billing Address')" \
		}, \
	    'shipping_address' : { \
		'label' : 'Shipping Address', \
		'type': 'VARCHAR', \
		'db_size' : '500', \
		'form_size' : '500', \
		'default' : "Institute for Scientific Research, Inc.\n119 Roush Circle, Industrial Park Road\nFairmont, WV 26554\nPhone: (304)368-9300\nFax:   (304)534-4106", \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine': 'checkLength', \
		'validation_arguments': ['form.shipping_address', 500, "'Shipping Address'", 1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Shipping Address')", \
		'lov' : "SELECT shipping_address FROM shipping_addresses ORDER BY shipping_address" \
		}, \
	    'date_requested' : { \
		'label' : 'Date Requested', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine': 'valid_date', \
		'validation_arguments': ["form.date_requested", "'Date Requested'", "true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Date Requested')", \
		'format': "MM-DD-YYYY" \
		}, \
	    'amount_requested' : { \
		'label' : 'Amount Requested', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments': ['form.amount_requested', "'Amount Requested'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Amount Requested')" \
		}, \
	    'date_needed_by' : { \
		'label' : 'Date Needed By', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments': ['form.date_needed_by', "'Date Needed By'", 1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Date Needed By')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'requisitioner' : { \
		'label' : 'Requisitioner', \
		'type': 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Requisitioner Username')", \
                'lov' : "SELECT last_name,first_name FROM project_members ORDER BY last_name" \

		}, \
            
            #'requisitioner_password' : { \
	#	'label' : 'Requisitioner Password', \
	#	'type': 'VARCHAR', \
	#	'db_size' : '8', \
	#	'form_size' : '8', \
	#	'default' : None, \
	#	'display' : 'hidden', \
	#		'form_input_type' : 'password', \
	#	'value' : '', \
	#	'display_order' : 11, \
	#	'required' : 1, \
	#	'leaveFocus' : None, \
	#	'gainFocus' : "displayHint('Requisitioner Password')" \
	#	}, \
	#    'requisitioner_signature' : { \
	#	'label' : 'Requisitioner Signature', \
	#	'type': 'VARCHAR', \
	#	'db_size' : '40', \
	#	'form_size' : '40', \
	#	'default' : None, \
	#	'display' : 'hidden', \
	#	'value' : '', \
	#	'display_order' : 12, \
	#	'leaveFocus' : None, \
        #	'gainFocus' : "displayHint('Requisitioner Signature')" \
	#	}, \
        #    'requisitioner_sig_function' : { \
	#	'label' : 'Signature Function', \
	#	'type': 'VARCHAR', \
	#	'db_size' : '5', \
	#	'form_size' : '5', \
	#	'default' : None, \
	#	'display' : 'hidden', \
	#	'value' : '', \
	#	'display_order' : 13, \
	#	'required' : 1, \
	#	'leaveFocus' : None, \
	#	'gainFocus' : "displayHint('Signature Function')", \
	#	'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
	#	}, \'''
	    'payment_method' : { \
		'label' : 'Payment Method', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Payment Method')", \
		'lov' : "SELECT payment_method FROM po_payment_method ORDER BY payment_method" \
		}, \
	    'subtotal' : { \
		'label' : 'Subtotal', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.subtotal', "'Subtotal'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Subtotal')" \
		}, \
	    'shipping_handling' : { \
		'label' : 'Shipping/Handling', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.shipping_handling', "'Shipping/Handling'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Shipping/Handling')" \
		}, \
	    'tax_exempt' : { \
		'label' : 'Tax Exempt', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 17, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.tax_exempt', "'Tax Exempt'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Tax Exempt')" \
		}, \
	    'po_total' : { \
		'label' : 'PO Total', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 18, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.po_total', "'PO Total'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Total')" \
		}, \
	    'quote_number' : { \
		'label' : 'Quote Number', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		#'required' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments': ['form.quote_number', "'Quote Number'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Quote Number')" \
		}, \
	    'direct_project_charge_number' : { \
		'label' : 'Direct Project Charge Number', \
		'type': 'VARCHAR', \
		'db_size' : '14', \
		'form_size' : '14', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 20, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.direct_project_charge_number", "'####-###-##-##'", "'Direct Project Charge Number'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Direct Project Charge Number')", \
		'format' : "####-###-##-##" \
		}, \
	    'direct_project_charge_amount' : { \
		'label' : 'Direct Project Charge Amount', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 21, \
		'validation_routine' : 'checkLength', \
		'validation_arguments': ['form.direct_project_charge_amount', 12,  "'Direct Project Charge Amount'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Direct Project Charge Amount')" \
		}, \
	    'direct_ra_username' : { \
		'label' : 'Direct Resource Authority Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 22, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Direct Resource Authority Username')" \
		}, \
	    'direct_ra_password' : { \
		'label' : 'Direct Resource Authority Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 23, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Direct Resource Authority Password')" \
		}, \
	    'direct_ra_signature' : { \
		'label' : 'Direct Resource Authority Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 24, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Direct Resource Authority Signature')" \
		}, \
	    'direct_ra_signature_function' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 25, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'direct_ra_signature_date' : { \
		'label' : 'Signature Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 26, \
		'validation_routine': 'valid_date', \
		'validation_arguments': ["form.direct_ra_signature_date", "'Signature Date'", "false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Date')", \
		'format' : "MM-DD-YYYY" \
		}, \
            'indirect_proj_charge_number' : { \
		'label' : 'Indirect Project Charge Number', \
		'type': 'VARCHAR', \
		'db_size' : '11', \
		'form_size' : '11', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 27, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.indirect_proj_charge_number", "'##-####-###'", "'Indirect Project Charge Number'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Indirect Project Charge Number')", \
		'format' : "##-####-###" \
		}, \
	    'indirect_proj_charge_amount' : { \
		'label' : 'Indirect Project Charge Amount', \
		'type': 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 28, \
		'validation_routine' : 'checkLength', \
		'validation_arguments': ['form.indirect_proj_charge_amount', 12,  "'Indirect Project Charge Amount'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Indirect Project Charge Amount')" \
		}, \
	    'indirect_ra_username' : { \
		'label' : 'Indirect Resource Authority Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 29, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Indirect Resource Authority Username')" \
		}, \
	    'indirect_ra_password' : { \
		'label' : 'Indirect Resource Authority Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 30, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Indirect Resource Authority Password')" \
		}, \
	    'indirect_ra_signature' : { \
		'label' : 'Indirect Resource Authority Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 31, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Indirect Resource Authority Signature')" \
		}, \
	    'indirect_ra_signature_function' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 32, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'indirect_ra_signature_date' : { \
		'label' : 'Signature Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 33, \
		'validation_routine': 'valid_date', \
		'validation_arguments': ["form.indirect_ra_signature_date", "'Signature Date'", "false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Date')", \
		'format' : "MM-DD-YYYY"  \
		}, \
	    'department_exec_username' : { \
		'label' : 'Department Executive Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 34, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Department Executive Username')" \
		}, \
	    'department_exec_password' : { \
		'label' : 'Department Executive Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
			'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 35, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Department Executive Password')" \
		}, \
	    'department_exec_signature' : { \
		'label' : 'Department Executive Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 36, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Department Executive Signature')" \
		}, \
	    'department_exec_sig_function' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 37, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'department_exec_sig_date' : { \
		'label' : 'Signature Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 38, \
		'validation_routine': 'valid_date', \
		'validation_arguments': ["form.department_exec_sig_date", "'Signature Date'", "false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Date')", \
		'format' : "MM-DD-YYYY", \
		}, \
	    'corporate_officer_username' : { \
		'label' : 'Corporate Officer Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 39, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Corporate Officer Username')" \
		}, \
	    'corporate_officer_password' : { \
		'label' : 'Corporate Officer Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 40, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Corporate Officer Password')" \
		}, \
	    'corporate_officer_signature' : { \
		'label' : 'Corporate Officer Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 41, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Corporate Officer Signature')" \
		}, \
	    'corp_officer_sig_function' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 42, 
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'corporate_officer_sig_date' : { \
		'label' :  'Signature Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 43, \
		'validation_routine': 'valid_date', \
		'validation_arguments': ["form.corporate_officer_sig_date", "'Signature Date'", "false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Date')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'comments' : { \
		'label' : 'Comments', \
		'type': 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 44, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.comments', 1024, "'Comments'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Comments')" \
		}, \
	    'po_math_checked_by_username' : { \
		'label' : 'PO Math Checked By Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 45, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Math Checked By Username')" \
		}, \
	    'po_math_checked_by_password' : { \
		'label' : 'PO Math Checked_By (Password)', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 46, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Math Checked By (Password)')" \
		}, \
	    'po_math_checked_by_signature' : { \
		'label' : 'PO Math Checked By Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 47, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Math Checked By Signature')" \
		}, \
	    'po_math_checked_by_sig_function' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 48, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'purchase_ordered_by_username' : { \
		'label' : 'Purchase Ordered By Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 49, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase Ordered By Username')" \
		}, \
	    'purchase_ordered_by_password' : { \
		'label' : 'Purchase Ordered By Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 50, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase Ordered By Password')" \
		}, \
	    'purchase_ordered_by_signature' : { \
		'label' : 'Purchase Ordered By Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 51, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase Ordered By Signature')" \
		}, \
	    'purchase_ordered_by_sig_func' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 52, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'purchase_ordered_date' : { \
		'label' : 'Date Ordered', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 53, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.purchase_ordered_date", "'Date Ordered'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Date Ordered')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'purchase_received_by_username' : { \
		'label' : 'Purchase Received By Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 54, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase received By Username')" \
		}, \
	    'purchase_received_by_password' : { \
		'label' : 'Purchase Received By Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 55, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase received By Password')" \
		}, \
	    'purchase_received_by_signature' : { \
		'label' : 'Purchase Received By Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 56, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase Received By Signature')" \
		}, \
	    'purchase_received_by_sig_func' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 57, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'purchase_received_date' : { \
		'label' : 'Purchase Received Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 58, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.purchase_received_date", "'Purchased received Date'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Purchase Received Date')", \
		'format' : "MM-DD-YYYY", \
		}, \
	    'date_invoice_received' : { \
		'label' : 'Date Invoice Received', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 59, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.date_invoice_received", "'Date Invoice Received'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Date Invoice Received')", \
		'format' : "MM-DD-YYYY", \
		}, \
	    'invoice_number' : { \
		'label' : 'Invoice Number', \
		'type': 'VARCHAR', \
		'db_size' : '15', \
		'form_size' : '15', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 60, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.invoice_number', 15, "'Invoice Number'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Invoice Number')" \
		}, \
	    'invoice_date' : { \
		'label' : 'Invoice Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 61, \
		'validation_routine' : 'valid_date',
		'validation_arguments' : ["form.invoice_date", "'Invoice Date'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Invoice Date')", \
		'format' : "MM-DD-YYYY", \
		}, \
	    'inv_math_checked_by_username' : { \
		'label' : 'Invoice Math Checked By Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 62, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Invoice Math Checked By Username')" \
		}, \
	    'inv_math_checked_by_password' : { \
		'label' : 'Invoice Math Checked By Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 63, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Invoice Math Checked By Password')" \
		}, \
	    'inv_math_checked_by_signature' : { \
		'label' : 'Invoice Math Checked By Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 64, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Invoice Math Checked By Signature')" \
		}, \
	    'inv_math_checked_by_sig_func' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 65, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'check_number' : { \
		'label' : 'Check Number', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 66, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.check_number', 4, "'Check Number'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Check Number')" \
		}, \
	    'check_date' : { \
		'label' : 'Check Date', \
		'type': 'DATE', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 67, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.check_date", "'Check Date'", 0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Check Date')", \
		'format' : "MM-DD-YYYY", \
		}, \
	    'ap_entered_by_username' : { \
		'label' : 'A/P Entered By Username', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 68, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('A/P Entered By Username')" \
		}, \
	    'ap_entered_by_password' : { \
		'label' : 'A/P Entered By Password', \
		'type': 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 69, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Invoice Math Checked By Signature')" \
		}, \
	    'ap_entered_by_signature' : { \
		'label' : 'A/P Entered By Signature', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 70, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('A/P Entered By Signature')" \
		}, \
	    'ap_entered_by_sig_function' : { \
		'label' : 'Signature Function', \
		'type': 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 71, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Signature Function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}}, \
	    #'property_id_number' : { \
		#'label' : 'Property ID #', \
		#'type': 'VARCHAR', \
		#'db_size' : '20', \
		#'form_size' : '20', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 72, \
		#'validation_routine' : 'checkLength', \
		#'validation_arguments' :['form.property_id_number', 20, "'Property ID #'", 0], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Property ID #')", \
		#}, \
	    #'prop_id_assigned_by_username' : { \
		#'label' : 'Property ID# Assigned By Username', \
		#'type': 'VARCHAR', \
		#'db_size' : '8', \
		#'form_size' : '8', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 73, \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Property ID# Assigned By Username')" \
		#}, \
	    #'prop_id_assigned_by_password' : { \
		#'label' : 'Property ID# Assigned By Password', \
		#'type': 'VARCHAR', \
		#'db_size' : '8', \
		#'form_size' : '8', \
		#'default' : None, \
		#'display' : 'editable', \
	        #'form_input_type': 'password', \
		#'value' : '', \
		#'display_order' : 74, \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Property ID# Assigned By Password')" \
		#}, \
	    #'prop_id_assigned_by_signature' : { \
		#'label' : 'Property ID# Assigned By Signature', \
		#'type': 'VARCHAR', \
		#'db_size' : '40', \
		#'form_size' : '40', \
		#'default' : None, \
		#'display' : 'read-only', \
		#'value' : '', \
		#'display_order' : 75, \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Property ID# Assigned By Signature')" \
		#}, \
	    #'prop_id_assigned_by_sig_func' : { \
		#'label' : 'Signature Function', \
		#'type': 'VARCHAR', \
		#'db_size' : '5', \
		#'form_size' : '5', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 76, \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Signature Function')", \
		#'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		#}, \
	    #'date_property_id_assigned' : { \
		#'label' : 'Date Property ID# Assigned ', \
		#'type': 'DATE', \
		#'db_size' : '10', \
		#'form_size' : '10', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 77, \
		#'validation_routine' : 'valid_date', \
		#'validation_arguments' : ["form.date_property_id_assigned", "'Date Property ID# Assigned'", 0], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Date Property ID# Assigned')", \
		#'format' : "MM-DD-YYYY", \
		#}, \
	    #'property_location' : { \
		#'label' : 'Property Location', \
		#'type': 'VARCHAR', \
		#'db_size' : '50', \
		#'form_size' : '50', \
		#'default' : None, \
		#'display' : 'editable', \
		#'value' : '', \
		#'display_order' : 78, \
		#'validation_routine' : 'checkLength', \
		#'validation_arguments' : ['form.property_location', 50, "'Property Location'", 0], \
		#'leaveFocus' : None, \
		#'gainFocus' : "displayHint('Property Location')" \
		#}}, \
	'po_line_item' : { \
	    'line_item' : { \
		'label' : 'Line Item', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.line_item',"'Line Item'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the line item type')" \
		}}, \
	'po_payment_method' : { \
	    'payment__method' : { \
		'label' : 'Payment Method', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.payment_method',"'Payment Method'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the payment method')" \
                }}, \
	'pai' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'Action Item Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Action Item Id')" \
		}, \
	    'gist' : { \
		'label' : 'Action Item GIST', \
		'type': 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.gist',"'Action Item Gist'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the gist of the action item')" \
		}, \
	    'ai_type' : { \
		'label' : 'Action Item Type', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the action item type')", \
                'lov' : "SELECT type_name FROM action_item_types ORDER BY type_name" \
		}, \
	    'date_created' : { \
		'label' : 'Date Created', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.date_created","'Date Created'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the action item was created')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'action_required' : { \
		'label' : 'Action Required', \
		'type' : 'VARCHAR', \
		'db_size' : '512', \
		'form_size' : '512', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.action_required',512,"'Action Required'",1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the action required')" \
		}, \
	    'originator' : { \
		'label' : 'Originator', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the originators name')", \
                'lov' : "SELECT last_name,first_name FROM project_members ORDER BY last_name" \
		}, \
	    'assigned_to' : { \
		'label' : 'Assigned To', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the name of the person action item is assigned to')", \
                'lov' : "SELECT last_name,first_name FROM project_members UNION SELECT 'All','' ORDER BY last_name" \
		}, \
	    'due_date' : { \
		'label' : 'Due Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the due date')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'recommended_action' : { \
		'label' : 'Recommended Action', \
		'type' : 'VARCHAR', \
		'db_size' : '512', \
		'form_size' : '512', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.recommended_action',512,"'Recommended Action'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the recommended action to take')" \
		}, \
	    'follow_up_status' : { \
		'label' : 'Follow-up Status', \
		'type' : 'VARCHAR', \
		'db_size' : '512', \
		'form_size' : '512', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.follow_up_status',512,"'Follow-up Status'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the follow-up status for the action')" \
		}, \
	    'completion_date' : { \
		'label' : 'Completion Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.completion_date',"'Completion Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the date the action was completed')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'completed_by' : { \
		'label' : 'Completed By', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter name of person who completed action')", \
		'lov' : "SELECT last_name,first_name FROM project_members ORDER BY last_name" \
		}}, \
	'task' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'Task Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Task Id')" \
		}, \
	    'description' : { \
		'label' : 'Description', \
		'type': 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.description',2048,"'Description'",1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a description of the task')" \
		}, \
	    'date_created' : { \
		'label' : 'Date Created', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.date_created","'Date Created'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the task was created')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'action_required' : { \
		'label' : 'Action Required', \
		'type' : 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.action_required',2048,"'Action Required'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the action required')" \
		}, \
	    'originator' : { \
		'label' : 'Originator', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the originators name')", \
                'lov' : "SELECT last_name,first_name FROM project_members ORDER BY last_name" \
		}, \
	    'assigned_to' : { \
		'label' : 'Assigned To', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the name of the person the task is assigned to')", \
                'lov' : "SELECT last_name,first_name FROM project_members UNION SELECT 'All','' ORDER BY last_name" \
		}, \
	    'due_date' : { \
		'label' : 'Due Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the due date')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'follow_up_status' : { \
		'label' : 'Follow-up Status', \
		'type' : 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.follow_up_status',2048,"'Follow-up Status'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the follow-up status for the task')" \
		}, \
	    'completion_date' : { \
		'label' : 'Completion Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.completion_date',"'Completion Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the date the task was completed')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'completed_by' : { \
		'label' : 'Completed By', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter name of person who completed the task')", \
		'lov' : "SELECT last_name, first_name FROM project_members ORDER BY last_name" \
		}}, \
	'spr' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'Problem Report Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Problem Report Id')" \
		}, \
	    'spr_prefix' : { \
		'label' : 'Prefix', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter prefix identifier for SPR')", \
		'lov' : "SELECT prefix FROM spr_prefixes ORDER BY prefix" \
		}, \
	    'outside_id' : { \
		'label' : 'Version Problem Found', \
		'type' : 'VARCHAR', \
		'db_size' : '15', \
		'form_size' : '15', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter outside id')" \
		}, \
	    'gist' : { \
		'label' : 'Problem GIST', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.gist',"'Problem Gist'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the gist of the problem')" \
		}, \
	    'source' : { \
		'label' : 'Version Problem Fixed', \
		'type' : 'VARCHAR', \
		'db_size' : '15', \
		'form_size' : '15', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter source of SPR')" \
		}, \
	    'spr_status' : { \
		'label' : 'Status', \
		'type' : 'VARCHAR', \
		'db_size' : '32', \
		'form_size' : '32', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter status of SPR')", \
		'lov' : "SELECT spr_status FROM spr_statuses ORDER BY spr_status" \
		}, \
	    'problem_description' : { \
		'label' : 'Problem Description', \
		'type' : 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.problem_description',2048,"'Problem Description'",1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the problem description')" \
		}, \
	    'problem_duplication' : { \
		'label' : 'Problem Duplication', \
		'type' : 'VARCHAR', \
		'db_size' : '3', \
		'form_size' : '3', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter problem duplication status')", \
		'lov' : "SELECT problem_duplication FROM problem_duplications ORDER BY problem_duplication" \
		}, \
	    'system_status' : { \
		'label' : 'System Status', \
		'type' : 'VARCHAR', \
		'db_size' : '15', \
		'form_size' : '15', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter system status')" \
		}, \
	    'priority' : { \
		'label' : 'Priority', \
		'type' : 'VARCHAR', \
		'db_size' : '51', \
		'form_size' : '51', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter priority of SPR')", \
		'lov' : "SELECT priority FROM spr_priorities ORDER BY priority" \
		}, \
	    'category' : { \
		'label' : 'Category', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter category of SPR')", \
		'lov' : "SELECT category FROM spr_categories ORDER BY category" \
		}, \
	    'originator' : { \
		'label' : 'Originator', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the originators name')", \
                'lov' : "SELECT last_name,first_name FROM project_members ORDER BY last_name" \
		}, \
	    'origination_date' : { \
		'label' : 'Origination Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.origination_date","'Origination Date'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the SPR was created')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'assigned_to' : { \
		'label' : 'Assigned To', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the last_name of the person assigned to SPR')", \
                'lov' : "SELECT last_name,first_name FROM project_members ORDER BY last_name" \
		}, \
	    'analysis' : { \
		'label' : 'Analysis', \
		'type' : 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.analysis',2048,"'Analysis'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the analysis of the problem')" \
		}, \
	    'analyst_username' : { \
		'label' : 'Analyst Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the analyst username')" \
		}, \
	    'analyst_password' : { \
		'label' : 'Analyst Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 17, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the analyst password')" \
		}, \
	    'analyst_signature' : { \
		'label' : 'Analyst Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 18, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the analyst')" \
		}, \
	    'analyst_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'swm_analysis_username' : { \
		'label' : 'Software Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 20, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Software Manager username')" \
		}, \
	    'swm_analysis_password' : { \
		'label' : 'Software Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 21, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Software Manager password')" \
		}, \
	    'swm_analysis_signature' : { \
		'label' : 'Software Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 22, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the Software Manager')" \
		}, \
	    'swm_analysis_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 23, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'corrective_action' : { \
		'label' : 'Corrective Action', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 24, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.corrective_action',1024,"'Corrective Action'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the corrective action of the problem')" \
		}, \
	    'config_items_impacted' : { \
		'label' : 'Configuration Items Impacted', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 25, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.config_items_impacted',1024,"'Configuration Items Impacted'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the configuration items impacted')" \
		}, \
	    'test_plan' : { \
		'label' : 'Test Plan', \
		'type' : 'VARCHAR', \
		'db_size' : '2048', \
		'form_size' : '2048', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 26, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.test_plan',2048,"'Test Plan'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the test plan')" \
		}, \
	    'test_results' : { \
		'label' : 'Test Results', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 27, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.test_results',1024,"'Test Results'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the test results')" \
		}, \
	    'swm_completion_username' : { \
		'label' : 'Software Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 28, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the software manager username')" \
		}, \
	    'swm_completion_password' : { \
		'label' : 'Software Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 29, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the software manager password')" \
		}, \
	    'swm_completion_signature' : { \
		'label' : 'Software Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 30, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the software manager')" \
		}, \
	    'swm_completion_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 31, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'test_completion_username' : { \
		'label' : 'Test Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 32, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the test manager username')" \
		}, \
	    'test_completion_password' : { \
		'label' : 'Test Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 33, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the test manager password')" \
		}, \
	    'test_completion_signature' : { \
		'label' : 'Test Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 34, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the test manager')" \
		}, \
	    'test_completion_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 35, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'cm_completion_username' : { \
		'label' : 'CM Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 36, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the cm manager username')" \
		}, \
	    'cm_completion_password' : { \
		'label' : 'CM Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 37, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the cm manager password')" \
		}, \
	    'cm_completion_signature' : { \
		'label' : 'CM Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 38, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the cm manager')" \
		}, \
	    'cm_completion_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 39, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'qa_completion_username' : { \
		'label' : 'QA Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 40, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the qa manager username')" \
		}, \
	    'qa_completion_password' : { \
		'label' : 'QA Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 41, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the qa manager password')" \
		}, \
	    'qa_completion_signature' : { \
		'label' : 'QA Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 42, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the qa manager')" \
		}, \
	    'qa_completion_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 43, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}}, \
	'ecp' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'ECP Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ECP Id')" \
		}, \
	    'ecp_prefix' : { \
		'label' : 'Prefix', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter prefix identifier for ECP')", \
		'lov' : "SELECT prefix FROM ecp_prefixes ORDER BY prefix" \
		}, \
	    'outside_id' : { \
		'label' : 'Outside Id', \
		'type' : 'VARCHAR', \
		'db_size' : '15', \
		'form_size' : '15', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter outside id')" \
		}, \
	    'ecp_type' : { \
		'label' : 'Type', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ECP type')", \
                'lov' : "SELECT type_name FROM ecp_types ORDER BY type_name" \
		}, \
	    'change_name' : { \
		'label' : 'Change Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.change_name',"'Change Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the change name')" \
		}, \
	    'ecp_status' : { \
		'label' : 'Status', \
		'type' : 'VARCHAR', \
		'db_size' : '32', \
		'form_size' : '32', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter status of ECP')", \
		'lov' : "SELECT ecp_status FROM ecp_statuses ORDER BY ecp_status" \
		}, \
	    'change_description' : { \
		'label' : 'Change Description', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.change_description',1024,"'Change Description'",1], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the change description')" \
		}, \
	    'originator' : { \
		'label' : 'Originator', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the originators name')", \
                'lov' : "SELECT last_name, first_name FROM project_members ORDER BY last_name" \
		}, \
	    'origination_date' : { \
		'label' : 'Origination Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.origination_date","'Origination Date'","true"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the ECP was created')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'analyst_username' : { \
		'label' : 'Analyst Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the analyst username')" \
		}, \
	    'analyst_password' : { \
		'label' : 'Analyst Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 11, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the analyst password')" \
		}, \
	    'analyst_signature' : { \
		'label' : 'Analyst Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 12, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the analyst')" \
		}, \
	    'analyst_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'analysis' : { \
		'label' : 'Analysis', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.analysis',1024,"'Analysis'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the analysis of the problem')" \
		}, \
	    'alternatives' : { \
		'label' : 'Alternatives/Impacts', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.alternatives',1024,"'Alternatives'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Alternatives/Impacts')" \
		}, \
	    'baseline_affected' : { \
		'label' : 'Baseline Affected', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.baseline_affected',1024,"'Baseline Affected'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Baseline Affected')" \
		}, \
	    'documentation_affected' : { \
		'label' : 'Documentation Affected', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 17, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.documentation_affected',1024,"'Documentation Affected'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Documentation Affected')" \
		}, \
	    'impacts_on_system' : { \
		'label' : 'Impacts on system', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 18, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.impacts_on_system',1024,"'Impacts on system'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the impacts on the system')" \
		}, \
	    'impacts_on_employment' : { \
		'label' : 'Impacts on Systems Employment', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.impacts_on_employment',1024,"'Impacts on Systems Employment'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Impacts on Systems Employment')" \
		}, \
	    'impacts_on_resources' : { \
		'label' : 'Impacts on System Resources', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 20, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.impacts_on_resources',1024,"'Impacts on System Resources'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the impacts on systems resources')" \
		}, \
	    'development_requirements' : { \
		'label' : 'Development Requirements', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 21, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.development_requirements',1024,"'Development Requirements'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the development requirements')" \
		}, \
	    'man_hour_estimate' : { \
		'label' : 'Man-Hour Estimate', \
		'type' : 'INT4', \
		'db_size' : '1', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 22, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.man_hour_estimate',"''","'Man-Hour Estimate'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Man-hour estimate')", \
		'format' : "#####" \
		}, \
	    'date_estimate' : { \
		'label' : 'Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 23, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.date_estimate","'Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date of estimate')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'implementation_point' : { \
		'label' : 'Recommended Implementation Point', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 24, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.implementation_point',1024,"'Recommended Implementation Point'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the recommended implementation point')" \
		}, \
	    'implementation_timing' : { \
		'label' : 'Implementation Timing Dependencies', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 25, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.implementation_timing',1024,"'Implementation Timing Dependencies'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the implementation timing dependencies')" \
		}, \
	    'related_spr_or_ecp' : { \
		'label' : 'Related SPR or ECP Number', \
		'type' : 'INT4', \
		'db_size' : '1', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 26, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.related_spr_or_ecp',"''","'Related SPR or ECP'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter related SPR or ECP Number')", \
		'format' : "#####" \
		}, \
	    'swm_analysis_username' : { \
		'label' : 'Software Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 27, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Software Manager username')" \
		}, \
	    'swm_analysis_password' : { \
		'label' : 'Software Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 28, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Software Manager password')" \
		}, \
	    'swm_analysis_signature' : { \
		'label' : 'Software Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 29, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the Software Manager')" \
		}, \
	    'swm_analysis_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 30, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'ccb_disposition' : { \
		'label' : 'Disposition', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 31, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the CCB disposition')", \
                'lov' : "SELECT disposition FROM dispositions ORDER BY disposition" \
		}, \
	    'implemented_until_date' : { \
		'label' : 'Implement/Deferred Until Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 32, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.implemented_until_date","'Implement/Deferred Until Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the to implement or defer to')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'ecp_number' : { \
		'label' : 'ECP Number', \
		'type' : 'INT4', \
		'db_size' : '1', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 33, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.ecp_number',"''","'ECP Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('ECP Number')", \
		'format' : "#####" \
		}, \
	    'ccb_comments' : { \
		'label' : 'CCB Comments', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 34, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.ccb_comments',1024,"'CCB Comments'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the CCB comments')" \
		}, \
	    'ccb_username' : { \
		'label' : 'CCB Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 35, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the CCB username')" \
		}, \
	    'ccb_password' : { \
		'label' : 'CCB Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 36, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the CCB Manager password')" \
		}, \
	    'ccb_signature' : { \
		'label' : 'CCB Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 37, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the CCB Manager')" \
		}, \
	    'ccb_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 38, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'gccb_disposition' : { \
		'label' : 'Disposition', \
		'type': 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 39, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the GCCB disposition')", \
                'lov' : "SELECT disposition FROM dispositions ORDER BY disposition" \
		}, \
	    'gccb_username' : { \
		'label' : 'GCCB Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 40, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the GCCB username')" \
		}, \
	    'gccb_password' : { \
		'label' : 'GCCB Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 41, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the GCCB Manager password')" \
		}, \
	    'gccb_signature' : { \
		'label' : 'GCCB Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 42, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the GCCB Manager')" \
		}, \
	    'gccb_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 43, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'disposition_received_date' : { \
		'label' : 'Disposition recevied from GCCB Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 44, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.disposition_received_date","'Disposition Received Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the disposition was received')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'date_closed' : { \
		'label' : 'Date Closed', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 45, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ["form.date_closed","'Date Closed'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter date the disposition was closed')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'swm_completion_username' : { \
		'label' : 'Software Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 46, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the software manager username')" \
		}, \
	    'swm_completion_password' : { \
		'label' : 'Software Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 47, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the software manager password')" \
		}, \
	    'swm_completion_signature' : { \
		'label' : 'Software Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 48, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the software manager')" \
		}, \
	    'swm_completion_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 49, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}, \
	    'qa_completion_username' : { \
		'label' : 'QA Manager Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 50, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the qa manager username')" \
		}, \
	    'qa_completion_password' : { \
		'label' : 'QA Manager Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 51, \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the qa manager password')" \
		}, \
	    'qa_completion_signature' : { \
		'label' : 'QA Manager Signature', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 52, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature of the qa manager')" \
		}, \
	    'qa_completion_signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 53, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')", \
		'lov' : "SELECT signature_function FROM signature_functions ORDER BY signature_function" \
		}}, \
        'us_states' : { \
	    'state_name' : { \
		'label' : 'State Full Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.state_name',"'State Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the state full name')" \
		}, \
	    'state_abbreviation' : { \
		'label' : 'State Abbreviation', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.state_abbreviation',"'State Abbreviation'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the state abbreviation')" \
		}}, \
	'problem_duplications' : { \
	    'problem_duplication' : { \
		'label' : 'Problem Duplication', \
		'type' : 'VARCHAR', \
		'db_size' : '3', \
		'form_size' : '3', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.problem_duplication',"'Problem Duplication'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the problem duplication')" \
		}}, \
	'member_roles' : { \
	    'member_role' : { \
		'label' : 'Member Role', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.member_role',"'Member Role'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the role of the member')" \
		}}, \
	'po_payment_method' : { \
	    'payment_method' : { \
		'label' : 'PO Payment Method', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.payment_method', "'PO Payment Method'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Payment Method')" \
		}}, \
	'po_line_item' : { \
	    'line_item' : { \
		'label' : 'PO line Item', \
		'type': 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.line_item', "'PO Line Item'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('PO Line Item')" \
		}}, \
	'categories' : { \
	    'category' : { \
		'label' : 'Category', \
		'type': 'VARCHAR', \
		'db_size' : '22', \
		'form_size' : '22', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.category', "'Category'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Category')" \
		}}, \
	'shipping_addresses' : { \
	    'shipping_address' : { \
		'label': 'Shipping Address', \
		'type':	'VARCHAR', \
		'db_size' : '80', \
		'form_size' : '80', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		#'validation_routine' : 'checkBlankField', \
		#'validation_arguments' : [form.shipping_address', "'Shipping Address'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Shipping Address')" \
		}}, \
	'spr_prefixes' : { \
	    'prefix' : { \
		'label' : 'Prefix', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.prefix',"'Prefix'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the prefix')" \
		}}, \
	'spr_statuses' : { \
	    'spr_status' : { \
		'label' : 'Status', \
		'type' : 'VARCHAR', \
		'db_size' : '32', \
		'form_size' : '32', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.spr_status',"'Status'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the status')" \
		}}, \
	'spr_priorities' : { \
	    'priority' : { \
		'label' : 'Priority', \
		'type' : 'VARCHAR', \
		'db_size' : '51', \
		'form_size' : '51', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.priority',"'Priority'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the priority')" \
		}}, \
	'spr_categories' : { \
	    'category' : { \
		'label' : 'Category', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.category',"'Category'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the category')" \
		}}, \
	'problem_duplications' : { \
	    'problem_duplication' : { \
		'label' : 'Problem Duplication', \
		'type' : 'VARCHAR', \
		'db_size' : '3', \
		'form_size' : '3', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.spr_problem_duplication',"'Problem Duplication'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the problem duplication')" \
		}}, \
	'signature_functions' : { \
	    'signature_function' : { \
		'label' : 'Signature Function', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.signature_function',"'Signature Function'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the signature function')" \
		}}, \
	'ecp_prefixes' : { \
	    'prefix' : { \
		'label' : 'ECP Prefix', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.prefix',"'ECP Prefix'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ECP prefix')" \
		}}, \
	'ecp_types' : { \
	    'type_name' : { \
		'label' : 'ECP Type', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.type_name',"'ECP Type'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ECP type')" \
		}}, \
	'ecp_statuses' : { \
	    'ecp_status' : { \
		'label' : 'ECP Status', \
		'type' : 'VARCHAR', \
		'db_size' : '32', \
		'form_size' : '32', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.ecp_status',"'ECP Status'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ECP status')" \
		}}, \
	'dispositions' : { \
	    'disposition' : { \
		'label' : 'Disposition', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.disposition',"'ECP Disposition'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the ECP disposition')" \
		}}, \
	'action_item_types' : { \
	    'type_name' : { \
		'label' : 'Type Name', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.type_name',"'Type Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the type name')" \
		}}, \
	'project_members' : { \
	    'id' : { \
		'db_constraints' : 'NOT NULL UNIQUE PRIMARY KEY', \
		'label' : 'Member Id', \
		'type': 'VARCHAR', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Member Id')" \
		}, \
	    'first_name' : { \
		'label' : 'First Name', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.first_name',"'First Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the first name')" \
		}, \
	    'last_name' : { \
		'label' : 'Last Name', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.last_name',"'Last Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the last name')" \
		}, \
	    'member_username' : { \
		'label' : 'Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.member_username',"'Username'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the username')" \
		}, \
	    'member_password' : { \
		'label' : 'Password', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
                'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
                'validation_routine' : 'checkBlankField', \
                'validation_arguments' : ['form.member_password',"'Password'"], \
                'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the users password')" \
		}, \
	    'member_role' : { \
		'label' : 'Member Role', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the role of the member')", \
		'lov' : "SELECT member_role FROM member_roles ORDER BY member_role" \
		}, \
	    'email' : { \
		'label' : 'E-mail Address', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'display_link' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.email',"'Email'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the members e-mail address')" \
		}, \
	    'company_name' : { \
		'label' : 'Company/Organization Name', \
		'type': 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.company_name',"'Company/Organization Name'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the Company/Organization Name')" \
		}, \
	    'address_line_1' : { \
		'label' : 'Address Line 1', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Address Line 1')" \
		}, \
	    'address_line_2' : { \
		'label' : 'Address Line 2', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Address Line 2')" \
		}, \
	    'city' : { \
		'label' : 'City', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
	    'state' : { \
		'label' : 'State', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM us_states ORDER BY state_abbreviation" \
		}, \
	    'zip' : { \
		'label' : 'Zip Code', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the zip code')" \
		}, \
	    'phone_number_voice' : { \
		'label' : 'Phone Number (Voice)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_voice","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the phone number (Voice)')", \
		'format' : "###-###-####" \
		}, \
	    'phone_extension' : { \
		'label' : 'Extension', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the extension')" \
		}, \
	    'cell_phone_number' : { \
		'label' : 'Cellular Phone Number', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.cell_phone_number","'###-###-####'","'Cellular Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the cellular phone number')", \
		'format' : "###-###-####" \
		}, \
	    'phone_number_fax' : { \
		'label' : 'Phone Number (FAX)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 17, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_fax","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the phone number (FAX)')", \
		'format' : "###-###-####" \
		},
	    'pgp_key' : { \
		'label' : 'PGP Key', \
		'type' : 'VARCHAR', \
		'db_size' : '1024', \
		'form_size' : '1024', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 18, \
		'validation_routine' : 'checkLength', \
		'validation_arguments' : ['form.pgp_key',1024,"'PGP Key'",0], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the user's PGP key')" \
		}}, \
	'priviledges' : { \
	    'member_username' : { \
		'label' : 'Username', \
		'type' : 'VARCHAR', \
		'db_size' : '8', \
		'form_size' : '8', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.member_username',"'Username'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the username')" \
		}, \
	    'upload' : { \
		'label' : 'Upload Files', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'del_docs' : { \
		'label' : 'Delete Data Items', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'list_docs' : { \
		'label' : 'View/Download Data Items', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'create_pai' : { \
		'label' : 'Create Action Items', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'del_pai' : { \
		'label' : 'Delete Action Items', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'create_spr' : { \
		'label' : 'Create Problem Reports', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'del_spr' : { \
		'label' : 'Delete Problem Reports', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'create_ecp' : { \
		'label' : 'Create Engineering Changes', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'del_ecp' : { \
		'label' : 'Delete Engineering Changes', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'folder_admin' : { \
		'label' : 'Create/Delete Document Folders', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'user_admin' : { \
		'label' : 'Add/Delete Users', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'cvs_web' : { \
		'label' : 'View CVS Web', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 18, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'cvs_export' : { \
		'label' : 'CVS Web Export', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'private_data' : { \
		'label' : 'View Private Data Items', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 20, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'pai_list' : { \
		'label' : 'Action Item Mailing List', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'spr_list' : { \
		'label' : 'Problem Report Mailing List', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'ecp_list' : { \
		'label' : 'Change Proposal Mailing List', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'edit_details' : { \
		'label' : 'Edit Document Details', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'project_data' : { \
		'label' : 'Edit Project Info', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 17, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		},
	    'view_task' : { \
		'label' : 'View Internal Tasks', \
		'type' : 'BOOL', \
		'db_size' : '6', \
		'form_size' : '6', \
		'default' : 'f', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 21, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter Yes or No')", \
		'format' : "Yes or No" \
		} }\
#	     'create_po' : { \
#		'label' : 'Create Purchase Order', \
#		'type' : 'BOOL', \
#		'db_size' : '6', \
#		'form_size' : '6', \
#		'default' : 'f', \
#		'display' : 'editable', \
#		'value' : '', \
#		'display_order' : 22, \
#		'leaveFocus' : None, \
#		'gainFocus' : "displayHint('Enter Yes or No')", \
#		'format' : "Yes or No" \
#		},
#	    'del_po' : { \
#		'label' : 'Delete Purchase Order', \
#		'type' : 'BOOL', \
#		'db_size' : '6', \
#		'form_size' : '6', \
#		'default' : 'f', \
#		'display' : 'editable', \
#		'value' : '', \
#		'display_order' : 23, \
#		'leaveFocus' : None, \
#		'gainFocus' : "displayHint('Enter Yes or No')", \
#		'format' : "Yes or No" \
#		} ,
#	     'create_inv' : { \
#		'label' : 'Create Inventory', \
#		'type' : 'BOOL', \
#		'db_size' : '6', \
#		'form_size' : '6', \
#		'default' : 'f', \
#		'display' : 'editable', \
#		'value' : '', \
#		'display_order' : 24, \
#		'leaveFocus' : None, \
#		'gainFocus' : "displayHint('Enter Yes or No')", \
#		'format' : "Yes or No" \
#		},
#	    'del_inv' : { \
#		'label' : 'Delete Inventory', \
#		'type' : 'BOOL', \
#		'db_size' : '6', \
#		'form_size' : '6', \
#		'default' : 'f', \
#		'display' : 'editable', \
#		'value' : '', \
#		'display_order' : 25, \
#		'leaveFocus' : None, \
#		'gainFocus' : "displayHint('Enter Yes or No')", \
#		'format' : "Yes or No" \
#		}} \"""
	}

    return data_tables
















