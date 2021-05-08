# get names of the files
name = input("Enter the filename: ")
rename = input("Enter the filename: ")

# open files
file1 = open(name,"r")
file2 = open(rename,"w")

# change file execution count
for line in file1.readlines():
    if "execution_count" in line:
        replace_line = '"execution_count": null,\n'
        file2.write(replace_line)
    else:
        file2.write(line+"\n")

# close files
file1.close()
file2.close()
