import re
import sys

def replace_val(match, params):
    if match.group(1) in params:
        return match.group(0).replace(match.group(0), params[match.group(1)])
    else:
        return match.group(0)

def hydrate_inputs(params, inputs):
    inputs_array = inputs.split('\n')
    replaced = []
    final = []

    # replace val's
    for i in inputs_array:
        replaced.append(re.sub(r'\{\{([^lb}]+)}\}', lambda m: replace_val(m, params), i))

    # replace lb's
    for i in replaced:
        final.append(re.sub(r'\{\{([lb}]+)}\}', lambda m:  re.sub("\{\{lb}}", '{', m.group(0)), i))

    return ''.join(final)

def hydrate_params(params):
    # sample regex: '((.*):)*\{\{([^lb}]+)}\}'
    params_obj = {}
    params_keys = []

    # build params object 
    params_array = params.split('\n')
    for i in params_array:
        key = re.search(r'.+?(?=:)', i).group(0)
        val = re.search(r'(?<=:).+', i).group(0)
        params_obj[key] = val
        params_keys.append(key)


    # match everything except lb's
    for i in params_keys:
        params_obj[i] = re.sub(r'\{\{([^lb}]+)}\}', lambda m: replace_val(m, params_obj), params_obj[i])
    
    # TODO: make this a loop instead of just running twice. If {{found}} run recursive function
    # match varaiables referencing other variables
    for i in params_keys:
        params_obj[i] = re.sub(r'\{\{([^lb}]+)}\}', lambda m: replace_val(m, params_obj), params_obj[i])

    # match lb's
    for i in params_keys:
        params_obj[i] = re.sub(r'\{\{([lb}]+)}\}', lambda m: re.sub("{\{lb}}", '{', m.group(0)), params_obj[i])

    return params_obj

def run_hydrator(inputs, params):
    try:
        # replace values in params
        updated_params = hydrate_params(params)

        # replace value in inputs
        updated_inputs = hydrate_inputs(updated_params, inputs)

        return updated_inputs
    except Exception as err:
        print('Error: ', err)
        return sys.exit(1)

def load_files(input_file, params_file):
    try:
        # read inputs file
        inputs_file_path = open(input_file)
        inputs = inputs_file_path.read()

        # read in params file
        params_file_path = open(params_file)
        params = params_file_path.read()

        result = run_hydrator(inputs, params)
        print(result)
        return result

    except Exception as err:
        print('Error reading file inputs, be sure to include inputs.txt as first arguement and params.txt as second argument: ', err)
        return sys.exit(1)

if __name__ == "__main__":
    input_file = sys.argv[1]
    params_file = sys.argv[2]
    load_files(input_file, params_file)