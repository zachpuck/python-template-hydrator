import re
import sys

inputs = """{{var1}} is good. {{var3}} {{var4}}, and {{var5}} are awesome.
test escaped braces: {{lb}}{{lb}}var3}}
vars{{var6}}workswithoutspaces.
Hello again {{var2}} and {{var1}}. {{var8}}"""

params = """var1:value1 {{var2}}
var2:{{lb}}{{lb}}var3}} equals {{var3}}
var3:value3
var4:{{lb}}{{lb}}var1}}: "{{var1}}"
var5:value5 even : can be used here
var6:{{var7}} doesnt exist!"""

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
    
    # match varaiables referencing other variables
    for i in params_keys:
        params_obj[i] = re.sub(r'\{\{([^lb}]+)}\}', lambda m: replace_val(m, params_obj), params_obj[i])

    # match lb's
    for i in params_keys:
        params_obj[i] = re.sub(r'\{\{([lb}]+)}\}', lambda m: re.sub("{\{lb}}", '{', m.group(0)), params_obj[i])

    return params_obj


def par_inputs(inputs, params):
    try:
      # 1) replace values in params
        updated_params = hydrate_params(params)
      
      # 2) replace value in inputs
        updated_inputs = hydrate_inputs(updated_params, inputs)

        return updated_inputs
    except Exception as err:
        print('Error: ', err)
        return sys.exit(1)
    
print(par_inputs(inputs, params))