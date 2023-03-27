





def format_file(file):
    with open(file, 'w')





 result = []
            with open('logs.log', 'r') as f:
                lines = f.readlines()
              
                for line in lines:
                    r = line.split('\t')
                    # print(r[1])
                    result.append({'levelname': r[0], 'asctime': r[1], 'message': r[2]})
            print(result)