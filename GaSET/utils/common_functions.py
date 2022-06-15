import os

def isStartWithGaSET(x):
    return not x.startswith('GaSET')



tested_project_names = ['FullMoonbirdsContract', 'Coomers', 'NOSTALGIA', 'GELON', 'KiddlesJPEGParty', 'BADPANDAS', 'SniperZuki', 'UwUNinjas', 'AiZuki', 'ROK']

# project 1
# project 5
# project 9
# project 10
# project 8
# project 3
# project 4
# project 7
# project 6
# project 2

def find_target_function_name(contract_name):
    function_name = 'none'
    function_start_line = -1
    function_end_line = -1

    if contract_name=='FullMoonbirdsContract':          # project 1
        function_name = 'Claim'
        function_start_line = 1296
        function_end_line = 1303
    elif contract_name=='Coomers':                      # project 5
        function_name = 'mint'
        function_start_line = 24
        function_end_line = 43
    elif contract_name=='NOSTALGIA':                    # project 9
        function_name = 'mint'
        function_start_line = 2238
        function_end_line = 2257
    elif contract_name=='GELON':                        # project 10
        function_name = '_transfer'
        function_start_line = 1094
        function_end_line = 1195
    elif contract_name=='KiddlesJPEGParty':             # project 8
        function_name = 'mint'
        function_start_line = 2235
        function_end_line = 2252
    elif contract_name=='BADPANDAS':                    # project 3
        function_name = 'mint'
        function_start_line = 1222
        function_end_line = 1236
    elif contract_name=='SniperZuki':                   # project 4
        function_name = 'mintNFTWhitelist'
        function_start_line = 1723
        function_end_line = 1736
    elif contract_name=='UwUNinjas':                    # project 7
        function_name = 'mint'
        function_start_line = 1337
        function_end_line = 1354
    elif contract_name=='AiZuki':                       # project 6
        function_name = 'mint'
        function_start_line = 1337
        function_end_line = 1354
    elif contract_name=='ROK':                          # project 2
        function_name = 'mintSaleNFT'
        function_start_line = 860
        function_end_line = 872

    return (function_name, function_start_line, function_end_line)


def execute(command):
    stream = os.popen(command)
    output = stream.read()

    return output


def gas_compare(first, second):
    return first['gas'] - second['gas']