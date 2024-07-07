from tkinter import *
from tkinter import filedialog
import warnings
import os
import csv

warnings.filterwarnings('ignore')
file=[]
initial_dir = "C:"
root = Tk()
root.title("CSV converter Interface")
root.geometry('800x300')

label1 = Label(root, text='input file')
label1.grid(row=1,column=0,sticky=W, padx=5, pady=5)
ent1 = Entry(root, width =90,font=('Helvetica',10))
ent1.grid(row=2, column=0,ipadx=10, ipady=5, padx=10, pady=5)

label2 = Label(root, text='report file')
label2.grid(row=3,column=0,sticky=W, padx=5, pady=5)
ent2 = Entry(root, width =90,font=('Helvetica',10))
ent2.grid(row=4, column=0,ipadx=10, ipady=5, padx=10, pady=5)

label3 = Label(root, text='Download File Location')
label3.grid(row=9,column=0,sticky=W, padx=5, pady=5)
ent3 = Entry(root, width =90,font=('Helvetica',10))
ent3.grid(row=10, column=0,ipadx=10, ipady=5, padx=10, pady=5)

def browsefunc1():
    filename = filedialog.askopenfilename(initialdir=initial_dir,
                                    defaultextension='.inp',
                                    filetypes=[
                                        ("Text file",".inp")
                                    ])

    ent1.insert(END, filename)
    file.append(filename)
    # print(file[0])

b1 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc1,
                             width = 10)
b1.grid(row=2, column=6)

def browsefunc2():
    filename = filedialog.askopenfilename(initialdir=initial_dir,
                                    defaultextension='.rpt',
                                    filetypes=[
                                        ("Text file",".rpt")
                                    ])

    ent2.insert(END, filename)
    file.append(filename)
    # print(file[0])

b2 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc2,
                             width = 10)
b2.grid(row=4, column=6)

def browsefunc3():
    filename = filedialog.askdirectory(title="Select Directory to Save CSV Files")
    ent3.insert(END,filename)
    file.append(filename)

b3 = Button(root, text="Browser", font=('Helvetica',10), command=browsefunc3,
                             width = 10)
b3.grid(row=10, column=6)

def save_file():
    inp_file = open(file[0], "r")
    rpt_file = open(file[1], "r")
    var = file[0].split("/")[-1].split('.')[0]
    input_file_name=file[2]+'/'+var
    inp_list = []

    default = '         0.0    0.0    0 00:00    0.0    0.0 \n'
    default = list(default.split())

    node_start = -1
    for index, line in enumerate(inp_file):

        if line[0:13] == '[COORDINATES]':
            node_start = index + 2

        if index > node_start and node_start != -1 and line[0:10] == '[VERTICES]':
            break

        if index > node_start and node_start != -1 and line != '\n':
            inp = list(line.split())
            inp_list.append(inp)

    inp_dic = {}

    for i in range(len(inp_list)):
        inp_dic.update({inp_list[i][0]: [inp_list[i][1], inp_list[i][2]]})

    final = []

    x_iter = iter(range(len(inp_list)))

    fld_start = -1

    # Calculation for Nodal Flooding Summary
    for index1, line1 in enumerate(rpt_file):

        if line1[2:23] == "Node Flooding Summary":
            fld_start = index1 + 9

        if index1 > fld_start and fld_start != -1 and line1 == '  \n':
            for j in x_iter:
                str_val = inp_list[j] + default
                final.append(str_val)
            break

        if index1 > fld_start and fld_start != -1 and line1 != '\n':

            rpt = str(list(line1.split())[0])

            for j in x_iter:
                inp = inp_list[j][0]
                if rpt == inp:
                    str_val = list(line1.split())
                    str_val.insert(1, inp_list[j][1])
                    str_val.insert(2, inp_list[j][2])
                    final.append(str_val)
                    break

                if rpt != inp:
                    str_val = inp_list[j] + default
                    final.append(str_val)
                    continue

    # Calculation for Nodal Inflow Summary
    x_iter = iter(range(len(inp_list)))
    inflow_start = -1
    rpt_file = open(file[1], "r")
    inflow_final = []

    for index1, line1 in enumerate(rpt_file):

        if line1[2:21] == "Node Inflow Summary":
            inflow_start = index1 + 8

        if index1 > inflow_start and inflow_start != -1 and line1 == '  \n':
            for j in x_iter:
                str_val = inp_list[j] + default
                inflow_final.append(str_val)
            break

        if index1 > inflow_start and inflow_start != -1 and line1 != '\n':

            rpt = str(list(line1.split())[0])
            for j in x_iter:
                inp = inp_list[j][0]
                if rpt == inp:
                    str_val = list(line1.split())
                    str_val.insert(1, inp_list[j][1])
                    str_val.insert(2, inp_list[j][2])

                    inflow_final.append(str_val)
                    break

                if rpt != inp:
                    str_val = inp_list[j] + default
                    inflow_final.append(str_val)
                    continue

    ##link related calculations
    x_iter = iter(range(len(inp_list)))
    link_start = -1
    inp_file = open(file[0], "r")
    link_final = []

    link_node_dic = {}
    for index, line in enumerate(inp_file):

        if line[0:10] == '[CONDUITS]':
            link_start = index + 2

        if index > link_start and link_start != -1 and line[0:11] == '[XSECTIONS]':
            break

        if index > link_start and link_start != -1 and line != '\n':
            inp = list(line.split())
            link_node_dic.update({inp[0]: [inp[1], inp[2]]})

    link_shp_start = -1
    link_junc_dic = {}
    inp_file = open(file[0], "r")

    for index, line in enumerate(inp_file):

        if line[0:11] == '[XSECTIONS]':
            link_shp_start = index + 2

        if index > link_shp_start and link_shp_start != -1 and line == '\n':
            break

        if index > link_shp_start and link_shp_start != -1 and line != '\n':
            inp = list(line.split())
            link_id = inp[0]
            corr_node_from = link_node_dic[link_id][0]
            corr_node_to = link_node_dic[link_id][1]
            corr_coor1 = inp_dic[corr_node_from][0]
            corr_coor2 = inp_dic[corr_node_from][1]
            node2_coor1 = inp_dic[corr_node_to][0]
            node2_coor2 = inp_dic[corr_node_to][1]

            inp.append(corr_coor1)
            inp.append(corr_coor2)
            inp.append(corr_node_from)
            inp.append(corr_node_to)
            inp.append(node2_coor1)
            inp.append(node2_coor2)

            # calculate square root distance
            link_length = ((float(corr_coor1) - float(node2_coor1)) ** 2 + (
                        float(corr_coor2) - float(node2_coor2)) ** 2) ** 0.5
            inp.append(str(link_length))

            # calculate average of node coordinates
            coordinate_x_average = (float(corr_coor1) + float(node2_coor1)) / 2
            coordinate_y_average = (float(corr_coor2) + float(node2_coor2)) / 2
            inp.append(str(coordinate_x_average))
            inp.append(str(coordinate_y_average))

            link_final.append(inp)
            link_junc_dic.update({link_id: link_final})

    ##get nodes from JUNCTIONS
    def junc_calc(start, end):
        junc_start = -1
        inp_file = open(file[0], "r")
        junc_lis = []

        for index, line in enumerate(inp_file):

            if line[0:len(start)] == start:
                junc_start = index + 2

            if index > junc_start and junc_start != -1 and line[0:len(end)] == end:
                break

            if index > junc_start and junc_start != -1 and line != '\n':
                inp = list(line.split())
                if len(inp) > 2 and not inp[0] == ';;Name' and not inp[0] == ';;--------------':
                    junc_node = inp[0]
                    bot_depth = float(inp[1])
                    max_depth = -1
                    for i in range(len(link_final)):
                        if (link_final[i][9] == junc_node) or (link_final[i][10] == junc_node):
                            if float(link_final[i][2]) > max_depth:
                                max_depth = float(link_final[i][2])
                    junc_x = inp_dic[junc_node][0]
                    junc_y = inp_dic[junc_node][1]
                    if max_depth != -1:
                        top_depth = bot_depth + max_depth
                        junc_line = [junc_node, junc_x, junc_y, bot_depth, top_depth, max_depth]
                    elif max_depth == -1:
                        junc_line = ["unknown error"]
                    junc_lis.append(junc_line)
        return junc_lis

    junctions_nodes = junc_calc('[JUNCTIONS]', '[OUTFALLS]')
    outfalls_nodes = junc_calc('[OUTFALLS]', '[CONDUITS]')
    junc_lis = junctions_nodes + outfalls_nodes

    with open(os.path.join(input_file_name + "_Flooding.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(final)

    with open(os.path.join(input_file_name + "_Inflow.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(inflow_final)

    with open(os.path.join(input_file_name + "_links.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(link_final)

    with open(os.path.join(input_file_name + "_junction.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(junc_lis)



b6 = Button(root, text="Save Text File", font=('Helvetica',8), command=save_file,
                             width = 80)
b6.grid(row=12,ipadx=15, ipady=10, padx=15, pady=10)
root.mainloop()
