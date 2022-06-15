from utils.common_functions import *
from functools import cmp_to_key

import os

# Get All Smart Contract Projects (A total of 10)
path = '../'
dir_list = os.listdir(path)
projects = list(filter(isStartWithGaSET, dir_list))

# linux
absolute_project_root_path = '/home/pingu/ase_2022' 

# windows
# absolute_project_root_path = 'E:\\jinyoung\\papers\\2022_ASE\\datasets'

# project 1
# project 5
# project 9
# project 6
# project 8
# project 3
# project 4
# project 7
# project 10
# project 2
tested_project_names = ['FullMoonbirdsContract', 'Coomers', 'NOSTALGIA', 'GELON', 'KiddlesJPEGParty', 'BADPANDAS', 'SniperZuki', 'UwUNinjas', 'AiZuki', 'ROK']
# motivation_project = ['ROK']
# Loop until last project
# len(projects)
for i in range(0, 1):
    # Select Each Projet
    project = projects[i]
    unoptimized_smart_contract_file = tested_project_names[i]

    # Make Project Path
    project_path = absolute_project_root_path + '/' + project + '/contracts'

    # Change Current Working Directory
    os.chdir(project_path)
    
    # Current Path
    current_path = os.getcwd()

    # Read Contract File
    unoptimized_smart_contract_content = open(current_path + '/' + unoptimized_smart_contract_file + '.sol', 'r')
    unoptimized_smart_contract_content = unoptimized_smart_contract_content.readlines()

    # Find Smart Contract Code line writed by Developer
    # Exclude library, ethereum standard
    developer_write_code_line = -1
    for j in range(0, len(unoptimized_smart_contract_content)):
        current_code = unoptimized_smart_contract_content[j]

        if "contract " + str(unoptimized_smart_contract_file) in current_code:
            developer_write_code_line = j
            # print(current_code)
            break
    
    
    if developer_write_code_line != -1:

        # First Step: Find Exceptions
        target_function_info = find_target_function_name(unoptimized_smart_contract_file)
        target_function_start_line = target_function_info[1]-1
        target_function_end_line = target_function_info[2]

        # 0 : name
        # 1 : start_line
        # 2 : end_line

        exception_lines = []
        exception_infos = []
        
        if target_function_info[0] != 'none':
            # Find exception lines
            for j in range(target_function_start_line, target_function_end_line+1):
                current_code = unoptimized_smart_contract_content[j].strip()

                if current_code.startswith('require('):
                    exception_lines.append(j)

            # Second Step: Exctract_feature
            for line_number in exception_lines:
                current_exception_code = unoptimized_smart_contract_content[line_number]
                current_exception_line = line_number
                temp_dict = dict()

                temp_dict['line'] = current_exception_line
                temp_dict['code'] = current_exception_code

                exception_infos.append(temp_dict)


            # Third Step: Find_Max_Location
            # Swap Location (From bottom line)
            temp_unoptimized_smart_contract_content = unoptimized_smart_contract_content
                
            original_transaction_gas = -1

            exception_infos = list(reversed(exception_infos))
            for j in range(0, len(exception_infos)):
                unchanged_code = temp_unoptimized_smart_contract_content

                current_exception = exception_infos[j]
                current_exception_line = current_exception['line']
                current_exception_code = current_exception['code']

                # Fourth Step: Oracle Test
                maximize_line = -1

                for k in range(current_exception_line, 0, -1):
                    current_before_code = temp_unoptimized_smart_contract_content[k-1]

                    if current_before_code.strip().startswith('require(') or current_before_code.strip().startswith('function ' + target_function_info[0] + '('):    
                        maximize_line = k
                        break
            
                if maximize_line != -1:
                    # Swap Code
                    temp_before_code = temp_unoptimized_smart_contract_content[maximize_line] # because start 0 index
               
                    temp_unoptimized_smart_contract_content[maximize_line] = current_exception_code
                    temp_unoptimized_smart_contract_content[current_exception_line] = temp_before_code

                    f = open('./Optimized' + unoptimized_smart_contract_file + '.sol', 'w')
                    f.writelines(temp_unoptimized_smart_contract_content)
                    f.close()

                    # Compile Error: Compile
                    execute_result = execute('truffle compile')

                    # Check Compile Success / Fail
                    if 'Compiled successfully using' in execute_result:
                        
                        print('Compile Success')
                    else:
                        temp_unoptimized_smart_contract_content = unchanged_code
                        print('Compile Fail')
                        continue

                    # Harmful Error: Test Case Pass
                    execute_result = execute('truffle test')
                    execute_results = execute_result.split('#GASET_GAS#')

                    print(execute_results)

                    # Original Transaction Gas
                    original_transaction_gas = execute_results[1]

                    # Check Pass Test Case
                    if '#GASET_GAS#' in execute_result:
                        print('Pass Test')
                    else:
                        temp_unoptimized_smart_contract_content = unchanged_code
                        print('Fail Test')

            # Fifth: gas_estimate
            # Estimate gas of each exception
            exception_gases = []

            origin_temp_unoptimized_smart_contract_content = []

            # Copy Code
            for j in range(0, len(temp_unoptimized_smart_contract_content)):
                origin_temp_unoptimized_smart_contract_content.append(temp_unoptimized_smart_contract_content[j])

            for j in range(0, len(exception_infos)):
                current_exception = exception_infos[j]
                current_exception_line = current_exception['line']
                current_exception_code = current_exception['code']

                temp_unoptimized_smart_contract_content[current_exception_line] = '//' + current_exception_code

                f = open('./Optimized' + unoptimized_smart_contract_file + '.sol', 'w')
                f.writelines(temp_unoptimized_smart_contract_content)
                f.close()

                # estimate real gas
                execute_result = execute('truffle test')
                
                execute_results = execute_result.split('#GASET_GAS#')

                # Non-Exception Transaction Gas
                transaction_gas = execute_results[1]

                # Each Exception's gas
                exception_gas = int(original_transaction_gas) - int(transaction_gas)
                
                temp_exception_gas_info = dict()
                temp_exception_gas_info['line'] = current_exception_line
                temp_exception_gas_info['code'] = current_exception_code
                temp_exception_gas_info['gas'] = exception_gas

                exception_gases.append(temp_exception_gas_info)

                temp_unoptimized_smart_contract_content = origin_temp_unoptimized_smart_contract_content

            
            real_exception_gases = []
            
            real_exception_gases.append(exception_gases[0])
            
            for j in range(1, len(exception_gases)):
                real_exception_gases.append(exception_gases[j])
                exception_gas = exception_gases[j]['gas']
                before_exception_gas = exception_gases[j-1]['gas']

                final_gas = exception_gas - before_exception_gas

                real_exception_gases[j]['gas'] = final_gas
            
            # print(real_exception_gases)

            min_max_exception_lines = []

            # find min_max line numbers
            for j in range(0, len(real_exception_gases)):
                exception_line = real_exception_gases[j]['line']
                min_max_exception_lines.append(exception_line)

            # Relocate Exception
            before_relocate_exception_gases = sorted(real_exception_gases, key=cmp_to_key(gas_compare))
            print(before_relocate_exception_gases)

            optimized_smart_contract_content = []

            # copy code
            for j in range(0, len(origin_temp_unoptimized_smart_contract_content)):
                optimized_smart_contract_content.append(origin_temp_unoptimized_smart_contract_content[j])


            print(min_max_exception_lines)

            for j in range(0, len(min_max_exception_lines)):
                unoptimized_exception_line = min_max_exception_lines[j]
                
                before_relocation_exception_code = before_relocate_exception_gases[j]['code']
                optimized_smart_contract_content[unoptimized_exception_line+1] = before_relocation_exception_code
            
            f = open('./Optimized' + unoptimized_smart_contract_file + '.sol', 'w')
            f.writelines(optimized_smart_contract_content)
            f.close()

            print("---finish---")