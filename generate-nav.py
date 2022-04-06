import os

ROOT_PREFIX = "docs/modules/ROOT/pages/"
DISTRIBUTION_PREFIX = ["community/", "enterprise/"]
parent_dirs = [ROOT_PREFIX]
for distribution in DISTRIBUTION_PREFIX:
    parent_dirs.append(distribution + ROOT_PREFIX)


def remove_substring(value:str, substring:str) -> str:
    return str(value).replace(substring, "")


def remove_substrings(value:str, substrings) -> str:
    output = value
    for substring in substrings:
        output = remove_substring(output, substring)
    return output


def make_xref(depth:int, file:str) -> str:
    file_partition = str(file).rpartition("/")
    filename = file_partition[len(file_partition)-1]
    filename = remove_substring(filename, ".adoc")
    return depth * "*" + " xref:" + file + "[" + filename + "]"


def dir_to_nav(parent, dir) -> str:
    output = ""
    for root, subdirs, files in os.walk(parent + dir, topdown=True):
        root = remove_substrings(root, DISTRIBUTION_PREFIX)
        root = remove_substring(root, ROOT_PREFIX) + "/"
        if(subdirs):
            for subdir in subdirs:
                output += "\n" + make_xref(str(root + subdir).count("/"), root + subdir)
                dir_to_nav(root, subdir)
        if(files):
            for file in files:
                output += "\n" + make_xref(str(root + file).count("/"), root + file)
    
    return output


for parent_dir in parent_dirs:
    nav_output = ""
    for dir in os.listdir(parent_dir):
        if(dir == "Technical Documentation"):
            continue
        if(os.path.isdir(parent_dir + dir)):
            nav_output += "\n\n." + dir
            nav_output += str(dir_to_nav(parent_dir, dir))
    print(nav_output)


    
    
#Find subdir
#Generate nav
#Replace snippet of nav in relevant location in nav.layout
#Move to next subdir
            
