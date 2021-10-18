from PIL import Image, ImageOps, ImageStat
from RavensProblem import RavensProblem
import numpy as np

# Types of Problem:
# 01 All Same
# 02 Union.  AUB == B or AUC ==C
# 03 Rotate     45,90, 135, 180, 235, 270
# 04 Mirror
# 05 Black Pixel Similarity_Difference_Etc.
# 06 Transformation

# Outline/Steps/Pseduo Code:
# Step 01: # initialize_2x2 (Create an Empty variable [] in init. Fill inside 2x2 or 3x3)
# #          initialize_3x3
# Step 02: Develop Helper Functions



class Agent:
    #################  Practice for B

    def __init__(self):
        # self.problem_name = None
        # self.log_file = None
        self.figure_names = ['A', 'B', 'C', '1', '2', '3', '4', '5', '6']
        self.options = [ '1', '2', '3', '4', '5', '6']
        self.images =  ['A', 'B', 'C']
        self.figure_pixel_matrix = {}
        # self.tversky_measure = {}
        # self.xor_measure = {}
        # self.figure_similarity = {}
        # self.figure_objects = {}

        self.figure_pixel_2d = {}
        self.option_score=dict.fromkeys(['1', '2', '3', '4', '5', '6'], 0)
        self.black_pixel_matrix = {}
        

    def initialize_2x2(self, problem: RavensProblem):

        # self.problem_name = None
        # self.log_file = None
        self.figure_names = ['A', 'B', 'C', '1', '2', '3', '4', '5', '6']
        self.options = ['1', '2', '3', '4', '5', '6']
        self.images = ['A', 'B', 'C']
        self.figure_pixel_matrix = {}
        # self.tversky_measure = {}
        # self.xor_measure = {}
        # self.figure_similarity = {}
        # self.figure_objects = {}

        self.figure_pixel_2d = {}
        self.option_score = dict.fromkeys(['1', '2', '3', '4', '5', '6'], 0)
        self.black_pixel_matrix = {}
        print(problem.name)
        #self.problem_name = problem.name
        folder_name = 'Problems/{}s {}/{}/'.format(problem.name.rsplit(' ', 1)[0], problem.name.split('-')[0].rsplit(' ', 1)[1], problem.name)
        for figure_name in self.figure_names:
            self.figure_pixel_2d[figure_name] = np.array(ImageOps.grayscale(Image.open('{}{}.png'.format(folder_name, figure_name))))

    # Helper Function Mirror/Reflect/Rotate 180
    def mirror(self, x):
        im_mirror = np.fliplr(x)
        return im_mirror

    def crop_reflect_merge(self, x):
        height, width = x.shape
        #print("X.shape ",x)
        #print(type(x))
        #img = Image.new("Grayscale", (x.width ))
        i1 = np.array(x[height-1, :width//2])
        i2 = np.array(x[height-1, width//2:])

        i1 = []
        #i1 = np.split(x, 92, axis=1)
        for i in range(x.shape[0]):
            for j in range(x.shape[1]//2):
                i1.append(x[i, j])
        i1 = np.reshape(np.array(i1), (184, 92))
        #print("i1 dim ", i1.shape)

        i2 = []
        for i in range(x.shape[0]):
            for j in range((x.shape[1]//2), x.shape[1]):
                i2.append(x[i, j])
        i2 = np.reshape(np.array(i2), (184, 92))
        #print("i2 dim ", i2.shape)


        im_1 = np.fliplr(i1)
        im_2 = np.fliplr(i2)

        #np.fliplr(img)

        #im_mirror_1 = ImageOps.mirror(im_1)
        #im_mirror_2 = ImageOps.mirror(im_2)

        #dst = Image.new('L', (im_mirror_1.width + im_mirror_2.width, im_mirror_1.height))
        #dst.paste(im1, (0, 0))
        #dst.paste(im2, (im1.width, 0))

        #new_img = Image.new("L")

        # merge = np.concatenate((im_1, im_2), axis=1)
        # img = Image.fromarray(merge)
        # img.save('my.png')
        # img.show()
        print("------Check Point 01----------")
        return np.concatenate((im_1, im_2), axis=1)

    def union(self, img1, img2):
        img3 = []
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                if img1[i, j] == 0 or img2[i, j] == 0:
                    img3.append(0)
                else:
                    img3.append(255)

        img3 = np.reshape(np.array(img3), (img1.shape[0], img1.shape[1]))
        img = Image.fromarray(img3)
        #img.show()
        return img3

    def intersection(self, img1, img2):
        img3 = []
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                if img1[i, j] == 0 and img2[i, j] == 0:
                    img3.append(0)
                else:
                    img3.append(255)

        img3 = np.reshape(np.array(img3), (img1.shape[0], img1.shape[1]))
        img = Image.fromarray(img3)
        #img.show()
        return img3

    def solve_by_union_of_two(self):
        union = {}

        for combination in [["A", "B"], ["A", "C"]]:
            union[combination[0] + combination[1]] = self.union(self.figure_pixel_2d[combination[0]],
                                                                self.figure_pixel_2d[combination[1]])
        #print("UNION\n", union)

        union["AB"] = self.union(self.figure_pixel_2d["A"], self.figure_pixel_2d["B"])
        union["AC"] = self.union(self.figure_pixel_2d["A"], self.figure_pixel_2d["C"])



        #IF A U B == B :
        #   for option in options:
        #       union ["C" + option] = C U option
        #FOR i in union :
        #   IF i == C:
        #       return int(i)

        max = 0
        best_answer = "-1"
        bothAB = 0
        bothAC = 0

        for k in range(184):
            for l in range(184):
                if union["AB"][k, l] == self.figure_pixel_2d["B"][k, l]:
                    bothAB += 1
                if union["AC"][k, l] == self.figure_pixel_2d["C"][k, l]:
                    bothAC += 1
        print("BOTHAB UNION: ", bothAB)
        if bothAB>33000 :
            #print("BOTHAB UNION: ", bothAB)
            for option in self.options:
                union["C"+option] = self.union(self.figure_pixel_2d["C"], self.figure_pixel_2d[option])
                both = 0
                for i in range(184):
                    for j in range(184):
                        if union["C" + option][i, j] == self.figure_pixel_2d[option][i, j]:
                            both += 1
                if both>max and both>33000:
                    max = both
                    best_answer = option
            return int(best_answer)



        return int(best_answer)

    def solve_by_mirror(self):

        A_mirror = self.mirror(self.figure_pixel_2d["A"])
        B_mirror = self.mirror(self.figure_pixel_2d["B"])
        C_mirror = self.mirror(self.figure_pixel_2d["C"])


        # Mirror B, C, Option
        # IF A == B_mirror :
        #   for option in options:
        #       If option = C_mirror
        # IF A == C_mirror :
        #   for option in options:
        #       If option = B_mirror


        max = 0
        best_answer = "-1"
        bothAB = 0
        bothAC = 0

        for k in range(self.figure_pixel_2d["A"].shape[0]):
            for l in range(self.figure_pixel_2d["A"].shape[0]):
                if A_mirror[k, l] == self.figure_pixel_2d["B"][k, l]:
                    bothAB += 1
                if A_mirror[k, l] == self.figure_pixel_2d["C"][k, l]:
                    bothAC += 1

        print("BothAB: ", bothAB)
        print("BothAC: ", bothAC)

        if bothAB>32100 :
            for option in self.options:
                #union["C"+option] = self.union(self.figure_pixel_2d["C"], self.figure_pixel_2d[option])
                both = 0
                for i in range(self.figure_pixel_2d["A"].shape[0]):
                    for j in range(self.figure_pixel_2d["A"].shape[0]):
                        if C_mirror[i, j] == self.figure_pixel_2d[option][i, j]:
                            both += 1
                if both>max and both>33000:
                    max = both
                    best_answer = option


        if bothAC>32100 :
            for option in self.options:
                #union["C"+option] = self.union(self.figure_pixel_2d["C"], self.figure_pixel_2d[option])
                both = 0
                for i in range(184):
                    for j in range(184):
                        if B_mirror[i, j] == self.figure_pixel_2d[option][i, j]:
                            both += 1
                if both>max and both>33000:
                    max = both
                    best_answer = option




        return int(best_answer)




    # def solve_by_union(self):
    #     options = ['1', '2', '3', '4', '5', '6', '7', '8']
    #     images = ["A", "B", "C", "D", "E", "F", "G", "H"]
    #     union = {}
    #     for combination in [["A", "B"], ["D", "E"], ["G", "H"]]:
    #         union[combination[0] + combination[1]] = self.union(self.figure_pixel_2d[combination[0]],
    #                                                             self.figure_pixel_2d[combination[1]])
    #     #print("Union\n", union)
    #     AB = 0
    #     DE = 0
    #     # imgGH = Image.fromarray(union["GH"])
    #     # imgGH.show()
    #     for i in range(184):
    #         for j in range(184):
    #             if(union["AB"][i, j] == self.figure_pixel_2d["C"][i, j]):
    #                 AB+=1
    #             if (union["DE"][i, j] == self.figure_pixel_2d["F"][i, j]):
    #                 DE+=1
    #     #print(f"AB: {AB}, DE: {DE}")
    #     if AB>33000 or DE>33000:
    #         #Search for umi['GH'] in options
    #         max = 0
    #         max_option = "-1"
    #         for i in options:
    #             a=0
    #             b=0
    #             both = 0
    #             for j in range(184):
    #                 for k in range(184):
    #                     if self.figure_pixel_2d[i][j, k] == union["GH"][j, k]:
    #                         both+=1
    #             if max<both and both>32000:
    #                 max = both
    #                 max_option = i
    #                 #print(f"Max: {max}, Option: {max_option}")
    #         return int(max_option)
    #     return -1



    # def union_minus_intersection(self):
    #     options = ['1', '2', '3', '4', '5', '6', '7', '8']
    #     images = ["A", "B", "C", "D", "E", "F", "G", "H"]
    #     umi = {}
    #     union = {}
    #     intersection = {}
    #     for combination in [["A", "B"], ["D", "E"], ["G", "H"]]:
    #         union[combination[0] + combination[1]] = self.union(self.figure_pixel_2d[combination[0]], self.figure_pixel_2d[combination[1]])
    #         intersection[combination[0] + combination[1]] = self.intersection(self.figure_pixel_2d[combination[0]], self.figure_pixel_2d[combination[1]])
    #         temp1 = []
    #         for i in range(union[combination[0]+combination[1]].shape[0]):
    #             for j in range(union[combination[0]+combination[1]].shape[1]):
    #                 if union[combination[0]+combination[1]][i, j] == 0 and intersection[combination[0] + combination[1]][i, j] == 0:
    #                     temp1.append(255)
    #                 elif union[combination[0]+combination[1]][i, j] == 255 and intersection[combination[0] + combination[1]][i, j] == 255:
    #                     temp1.append(255)
    #                 else :
    #                     temp1.append(0)
    #         temp1 = np.reshape(np.array(temp1), (184, 184))
    #         umi[combination[0] + combination[1]] = temp1
    #
    #     similarity = {}
    #     # if (umi["AB"] and self.figure_pixel_2d["C"] are very similar) and (umi["DE"] and self.figure_pixel_2d["F"] are very similar):
    #     #     search for umi["GH"] in options and select the most similar one above a specific threshold
    #     AB=0
    #     DE=0
    #     GH=0
    #     # imgAB = Image.fromarray(umi["AB"])
    #     # imgDE = Image.fromarray(umi["DE"])
    #     # imgGH = Image.fromarray(umi["GH"])
    #     # imgAB.show()
    #     # imgDE.show()
    #     # imgGH.show()
    #
    #     for i in range(184):
    #         for j in range(184):
    #             if(umi["AB"][i, j] == self.figure_pixel_2d["C"][i, j]):
    #                 AB+=1
    #             if (umi["DE"][i, j] == self.figure_pixel_2d["F"][i, j]):
    #                 DE+=1
    #             #if(umi["AB"][i, j] == self.figure_pixel_2d["C"][i, j]):
    #     #print(f"AB: {AB}, DE: {DE}")
    #     if AB>32000 or DE>32000:
    #         #Search for umi['GH'] in options
    #         max = 0
    #         max_option = "-1"
    #         for i in options:
    #             a=0
    #             b=0
    #             both = 0
    #             for j in range(184):
    #                 for k in range(184):
    #                     if self.figure_pixel_2d[i][j, k] == umi["GH"][j, k]:
    #                         both+=1
    #             if max<both and both>30000:
    #                 max = both
    #                 max_option = i
    #         return int(max_option)
    #     return -1

#######################AREA DIFFERENCE FUNCTION NEEDED#################
    def all_same(self):
        options = ['1', '2', '3', '4', '5', '6']
        images = ["A", "B", "C"]
        duplicate = dict.fromkeys(["A", "B", "C"], -1)
        for i in images:
            pix_mean1 = ImageStat.Stat(Image.fromarray(self.figure_pixel_2d[i])).mean
            max = 0
            for j in options:
                pix_mean2 = ImageStat.Stat(Image.fromarray(self.figure_pixel_2d[j])).mean
                # print("pix mean 1: ", pix_mean1[0])
                # print("pix mean 2", pix_mean2[0])
                a = 0
                b = 0
                both = 0

                for k in range(self.figure_pixel_2d[i].shape[0]):
                    for l in range(self.figure_pixel_2d[i].shape[1]):
                        if self.figure_pixel_2d[i][k, l] == self.figure_pixel_2d[j][k, l]:
                            both += 1

                if max < both and both > 32000:
                    max = both
                    duplicate[i] = j
                # print(f"BOTH {i},{j}: {both}")
                # if pix_mean1[0] == pix_mean2[0]:
                #     #print("True")
                #     duplicate[i] = j
                #     break
                #     #print(duplicate[i])
            # print("DUPLICATE\n",duplicate)
        s = set(duplicate.values())
        count = {}
        for x in s:
            count[x] = sum(value == x for value in duplicate.values())
        count = dict(sorted(count.items(), key=lambda item: item[1]))
        count = list(count.items())
        # print("Count\n", count)
        if len(count) == 1 and count[0][1] == 3 :
            return int(count[0][0])

        # freq = {}
        # for items in duplicate:
        #     freq[items.value] = duplicate.count(items.value)
        #        print("freq\n", freq)
        return -1

    def matching_combination(self):
        options = ['1', '2', '3', '4', '5', '6']
        images = ["A", "B", "C"]
        duplicate = dict.fromkeys(["A", "B", "C"], -1)

        for i in images:
            pix_mean1 = ImageStat.Stat(Image.fromarray(self.figure_pixel_2d[i])).mean
            max = 0
            for j in options:
                pix_mean2 = ImageStat.Stat(Image.fromarray(self.figure_pixel_2d[j])).mean
                #print("pix mean 1: ", pix_mean1[0])
                #print("pix mean 2", pix_mean2[0])
                a = 0
                b = 0
                both = 0

                for k in range(self.figure_pixel_2d[i].shape[0]):
                    for l in range(self.figure_pixel_2d[i].shape[1]):
                        if self.figure_pixel_2d[i][k, l] == self.figure_pixel_2d[j][k, l]:
                            both += 1

                if max < both and both > 32000:
                    max = both
                    duplicate[i] = j
                #print(f"BOTH {i},{j}: {both}")
                # if pix_mean1[0] == pix_mean2[0]:
                #     #print("True")
                #     duplicate[i] = j
                #     break
                #     #print(duplicate[i])
        #print("DUPLICATE\n",duplicate)
        s = set(duplicate.values())
        count = {}
        for x in s:
            count[x] = sum(value == x for value in duplicate.values())
        count = dict(sorted(count.items(), key=lambda item: item[1]))
        count = list(count.items())
        #print("Count\n", count)
        if len(count) == 3 and count[1][1] == 3 and count [2][1] == 3:
            return int(count[0][0])

        # freq = {}
        # for items in duplicate:
        #     freq[items.value] = duplicate.count(items.value)
        # print("freq\n", freq)
        return -1


    def black_pixel_counter(self, image):
        count = 0
        for i in range(184):
            for j in range(184):
                if image[i, j] == 0:
                    count += 1
        return count

    def similarity_of_two_number(self, n1, n2):
        if n1 + n2 == 0:
            return 0
        return abs(n1 - n2) / ((n1 + n2) / 2)

    def crop_reflect_merge(self, x):
        height, width = x.shape
        #print("X.shape ",x)
        #print(type(x))
        #img = Image.new("Grayscale", (x.width ))
        i1 = np.array(x[height-1, :width//2])
        i2 = np.array(x[height-1, width//2:])

        i1 = []
        #i1 = np.split(x, 92, axis=1)
        for i in range(x.shape[0]):
            for j in range(x.shape[1]//2):
                i1.append(x[i, j])
        i1 = np.reshape(np.array(i1), (184, 92))
        #print("i1 dim ", i1.shape)

        i2 = []
        for i in range(x.shape[0]):
            for j in range((x.shape[1]//2), x.shape[1]):
                i2.append(x[i, j])
        i2 = np.reshape(np.array(i2), (184, 92))

        im_1 = np.fliplr(i1)
        im_2 = np.fliplr(i2)

        return np.concatenate((im_1, im_2), axis=1)

    # def method_half_cropped_reflect(self):
    #     # Check if A and C black pixel count similar and check if A crop_reflect_merge similar to C (Matching_Combination)
    #     reflection_dict = {}
    #     count_dict = {}
    #     AC = (abs(self.black_pixel_matrix["A"] - self.black_pixel_matrix["C"]))
    #     print("AC: ", AC)
    #     FD = (abs(self.black_pixel_matrix["F"] - self.black_pixel_matrix["D"]))
    #     print("FD: ", FD)
    #
    #     if AC<=100 and FD<=100:
    #         reflection_dict["A"] = self.crop_reflect_merge(self.figure_pixel_2d["A"])
    #         reflection_dict["D"] = self.crop_reflect_merge(self.figure_pixel_2d["D"])
    #         #print("REFLECTION DICT\n", reflection_dict)
    #
    #         bothC = 0
    #         bothF = 0
    #
    #         for i in range(184):
    #             for j in range(184):
    #                 if reflection_dict["A"][i, j] == self.figure_pixel_2d["C"][i, j]:
    #                     bothC += 1
    #                 if reflection_dict["D"][i, j] == self.figure_pixel_2d["F"][i, j]:
    #                     bothF += 1
    #         count_dict["A"] = bothC
    #         count_dict["D"] = bothF
    #
    #         print("Count Dict\n", count_dict)
    #
    #         if count_dict["A"] > 30000 and count_dict["D"] > 30000:
    #             reflection_dict["G"]  = self.crop_reflect_merge(self.figure_pixel_2d["G"])
    #             count_dict = {}
    #             for option in self.options:
    #                 both = 0
    #                 for i in range(184):
    #                     for j in range(184):
    #                         if reflection_dict["G"][i, j] == self.figure_pixel_2d[option][i, j]:
    #                             both+=1
    #                 count_dict[option] = both
    #             print("Count Dict\n",count_dict)
    #             best_answer = max(count_dict, key=count_dict.get)
    #             if count_dict[best_answer] >= 30000 :
    #                 return int(best_answer)
    #     return -1



    # def method_simpler_pixel_difference_similarity(self):
    #     best_answer = "-1"
    #     row_1 = abs(self.black_pixel_matrix["C"] - self.black_pixel_matrix["A"])
    #     #print("ROW1: ", row_1)
    #     #print("Black Pixel Count A\n", self.black_pixel_matrix["A"])
    #     row_2 = abs(self.black_pixel_matrix["F"] - self.black_pixel_matrix["D"])
    #     #print("ROW2: ", row_2)
    #     #print("Black Pixel Count D\n", self.black_pixel_matrix["D"])
    #
    #     similarity_score = {}
    #     if (abs(row_1 - self.black_pixel_matrix["A"]) <= 100 and abs(row_2 - self.black_pixel_matrix["D"]) <= 100):
    #         for option in self.options:
    #             similarity_score[option] = abs(abs(self.black_pixel_matrix[option] - self.black_pixel_matrix["G"]) - self.black_pixel_matrix["G"])
    #         #print("Similarity Score\n", similarity_score)
    #         best_answer = min(similarity_score, key=similarity_score.get)
    #         second_best_answer = list(sorted(similarity_score.values()))[-1]
    #     if best_answer != "-1" and similarity_score[best_answer] <= 100 :
    #         return int(best_answer)
    #
    #     return int(best_answer)

    def method_vertical_flip(self):
        best_answer = "-1"

        A_mirror = np.flipud(self.figure_pixel_2d["A"])
        B_mirror = np.flipud(self.figure_pixel_2d["B"])
        C_mirror = np.flipud(self.figure_pixel_2d["C"])

        a_sim_c = 0

        # print("Figure A:\n")
        # print(A_mirror.shape)
        # for i in range(len(A_mirror)):
        #     for j in range(len(A_mirror)):
        #         print(self.figure_pixel_2d["A"][i][j], end=" ")
        #     print("\n")

        for i in range(len(self.figure_pixel_2d["A"])):
            for j in range(len(self.figure_pixel_2d["B"])):
                if(self.figure_pixel_2d["A"][i][j] == C_mirror[i][j]):
                    a_sim_c += 1

        print("A SIM C: ", a_sim_c)
        if a_sim_c>=33000:
            similarity = dict.fromkeys(self.options, 0)
            temp = 0
            for option in self.options:
                for i in range(len(B_mirror)):
                    for j in range(len(B_mirror)):
                        if (B_mirror[i][j] ==  self.figure_pixel_2d[option][i][j]):
                            temp+=1
                similarity[option] = temp
                temp = 0

            max_key = max(similarity, key=similarity.get)
            if similarity[max_key] >= 33000:
                best_answer = max_key
        return int(best_answer)

    def method_pixel_difference_similarity(self):
        best_answer = "-1"
        #IF pixel_count(C-B) == pixel_count(B-A) and pixel_count(F-E) == pixel_count(E-D):
        #   for option in options :
        #       if pixel_count(option-H) == pixel_count(H-G):
        #           return int(option)
        #2652
        #print("Black Pixel Matrix\n", self.black_pixel_matrix)
        row_1 = abs((self.black_pixel_matrix["B"] - self.black_pixel_matrix["A"]))
        #print("ROW 1: ", row_1)
        #print("ROW 2: ", row_2)

        similarity_score = {}

        if row_1 <= 200:
            for option in self.options:
                op_H = abs((self.black_pixel_matrix[option] - self.black_pixel_matrix["H"]) - (self.black_pixel_matrix["H"] - self.black_pixel_matrix["G"]))
                #print(f"OPTION:{option}HG: {op_H}")
                similarity_score[option] = op_H
                # if  op_H <= 300:
                #     best_answer = option
                #     return int(best_answer)
            possible_answer = min(similarity_score, key=similarity_score.get)
            second_best_answer = list(sorted(similarity_score.values()))[1]
            #print("Second Best Answer\n", second_best_answer)
            if similarity_score[possible_answer] <= 300 and second_best_answer > 300:
                best_answer = possible_answer
                return int(possible_answer)
        return int(best_answer)

    # def method_change_of_area_to_get_third(self):
    #     best_answer = -1
    #     similarity_maximum = 0
    #     options = ['1', '2', '3', '4', '5', '6', '7', '8']
    #     black_pixel_difference = {}
    #     first_row = ['A', 'B', 'C']
    #     second_row = ['D', 'E', 'F']
    #
    #     #possible_combinations = self.permutations(first_row, second_row)
    #     possible_combinations = (dict(zip(first_row, b)) for b in itertools.permutations(second_row, len(first_row)))
    #     #print("Black Pixel Matrix\n", self.black_pixel_matrix)
    #     similarity_of_combination = {}
    #
    #     for combination in possible_combinations:
    #         correspondence = list(combination.items())
    #         black_pixel_difference[correspondence[0][0]+correspondence[0][1]] = self.similarity_of_two_number(abs(self.black_pixel_matrix[correspondence[0][0]] - self.black_pixel_matrix[correspondence[1][0]]), abs(self.black_pixel_matrix[correspondence[0][1]] - self.black_pixel_matrix[correspondence[1][1]]))
    #         black_pixel_difference[correspondence[1][0]+correspondence[1][1]] = self.similarity_of_two_number(abs(self.black_pixel_matrix[correspondence[1][0]] - self.black_pixel_matrix[correspondence[2][0]]), abs(self.black_pixel_matrix[correspondence[1][1]] - self.black_pixel_matrix[correspondence[2][1]]))
    #         black_pixel_difference[correspondence[2][0]+correspondence[2][1]] = self.similarity_of_two_number(abs(self.black_pixel_matrix[correspondence[0][0]] - self.black_pixel_matrix[correspondence[2][0]]), abs(self.black_pixel_matrix[correspondence[0][1]] - self.black_pixel_matrix[correspondence[2][1]]))
    #
    #         similarity_of_combination[frozenset(combination.items())] = statistics.mean(black_pixel_difference.values())
    #     #print("Black Pixel Difference\n", black_pixel_difference)
    #     most_likely = min(similarity_of_combination.items(), key=lambda x: x[1])
    #     unique = sum(map((most_likely[1]).__eq__, similarity_of_combination.values()))
    #
    #     if most_likely[1] <= 0.3 and unique == 1:
    #         similarity_of_combination = {}
    #         for possible_answer in options:
    #             if ('A', 'D') in most_likely[0] and ('B', 'E') in most_likely[0] and ('C', 'F') in most_likely[0]:
    #                 combination = {'A': 'G', 'B': 'H', 'C': possible_answer}
    #                 # print(combination)
    #             elif ('A', 'E') in most_likely[0] and ('B', 'F') in most_likely[0] and ('C', 'D') in most_likely[0]:
    #                 combination = {'A': possible_answer, 'B': 'G', 'C': 'H'}
    #                 # print(combination)
    #             else:
    #                 return -1
    #
    #             black_pixel_difference = {}
    #             correspondence = list(combination.items())
    #             black_pixel_difference[correspondence[0][0] + correspondence[0][1]] = self.similarity_of_two_number(
    #                 abs(self.black_pixel_matrix[correspondence[0][0]] - self.black_pixel_matrix[correspondence[1][0]]),
    #                 abs(self.black_pixel_matrix[correspondence[0][1]] - self.black_pixel_matrix[correspondence[1][1]]))
    #             black_pixel_difference[correspondence[1][0] + correspondence[1][1]] = self.similarity_of_two_number(
    #                 abs(self.black_pixel_matrix[correspondence[1][0]] - self.black_pixel_matrix[correspondence[2][0]]),
    #                 abs(self.black_pixel_matrix[correspondence[1][1]] - self.black_pixel_matrix[correspondence[2][1]]))
    #             black_pixel_difference[correspondence[2][0] + correspondence[2][1]] = self.similarity_of_two_number(
    #                 abs(self.black_pixel_matrix[correspondence[0][0]] - self.black_pixel_matrix[correspondence[2][0]]),
    #                 abs(self.black_pixel_matrix[correspondence[0][1]] - self.black_pixel_matrix[correspondence[2][1]]))
    #
    #             similarity_of_combination[frozenset(combination.items())] = statistics.mean(
    #                 black_pixel_difference.values())
    #             print("Similarity of Combination\n", similarity_of_combination)
    #         most_likely = min(similarity_of_combination.items(), key=lambda x: x[1])[0]
    #         most_likely = set(most_likely)
    #         print("Most Likely\n", most_likely)
    #         for x in most_likely:
    #             print("X: ", x)
    #             for j in x:
    #                  if j in options:
    #                     return int(j)
    #
    #         return  -1
    #     return -1


    # def tversky_score(self, temp1, temp2):
    #
    #     onlyB = 0
    #     onlyA = 0
    #     ABboth = 0
    #
    #     for i in range(temp1.shape[0]):
    #         for j in range(temp1.shape[1]):
    #             if temp1[i,j] == 0 and temp2[i,j] == 0:
    #                 ABboth += 1
    #             elif temp1[i,j] == 0 and temp2[i,j] == 255:
    #                 onlyA += 1
    #             elif temp1[i,j] == 255 and temp2[i,j] == 0:
    #                 onlyB += 1
    #
    #     #print(f"OnlyA : {onlyA}, OnlyB: {onlyB}, ABboth : {ABboth}")
    #     raven_score = 0
    #     if onlyA != 0 or onlyB != 0 or ABboth != 0:
    #         raven_score = (2 * ABboth) / (onlyA + onlyB + 2 * ABboth)
    #     #print("Raven_Score: ", raven_score)
    #     return raven_score
    # def tversky_index(self):
    #     best_answer = -1
    #     self.figure_objects = {}
    #     self.tversky_measure_identity = {}
    #     self.identity_difference = {}#dict.fromkeys(['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'], 0)
    #     self.option_score = dict.fromkeys(['1', '2', '3', '4', '5', '6', '7', '8'], 0)
    #     for combination in [['A','B'],['G', 'H'],['B', 'C'],['D', 'E'],['E', 'F'], ['H','1'], ['H','2'], ['H','3'], ['H','4'], ['H','5'], ['H','6'], ['H','7'], ['H','8'], ['A', 'C'], ['D', 'F'], ['G', '1'], ['G', '2'], ['G', '3'], ['G', '4'], ['G', '5'], ['G', '6'], ['G', '7'], ['G', '8']]:
    #         self.tversky_measure_identity[combination[0] + combination[1]] = self.tversky_score(self.figure_pixel_2d[combination[0]], self.figure_pixel_2d[combination[1]])
    #     print("Tversky Measure Identity\n", self.tversky_measure_identity)
    #     for combination in [['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6'],
    #                         ['H', '7'], ['H', '8']]:# ['G', '1'], ['G', '2'], ['G', '3'], ['G', '4'],
    #                         #['G', '5'], ['G', '6'], ['G', '7'], ['G', '8']]:
    #         if combination[0] == 'H' :
    #             if(self.tversky_measure_identity[combination[0]+combination[1]]!=0 ):
    #                 a=0
    #                 b=0
    #                 if self.tversky_measure_identity['BC']!=0:
    #                     a = (1 - abs((self.tversky_measure_identity['AB'] / self.tversky_measure_identity['BC']) - (self.tversky_measure_identity['GH'] / self.tversky_measure_identity[combination[0] + combination[1]])))
    #                 if self.tversky_measure_identity['EF'] != 0:
    #                     b = (1 - abs((self.tversky_measure_identity['DE'] / self.tversky_measure_identity['EF']) - (
    #                                 self.tversky_measure_identity['GH'] / self.tversky_measure_identity[
    #                             combination[0] + combination[1]])))
    #                 self.identity_difference[combination[1]] = a+b
    #             # self.identity_difference[combination[0]+combination[1]] = abs(self.tversky_measure_identity['BC']-self.tversky_measure_identity[combination[0]+combination[1]])
    #             # self.identity_difference[combination[0]+combination[1]] += abs(self.tversky_measure_identity['EF']-self.tversky_measure_identity[combination[0]+combination[1]])
    #
    #             #
    #             else:
    #                 self.identity_difference[combination[1]] = 0
    #
    #         # if combination[0] == 'G':
    #         #     self.identity_difference[combination[0]+combination[1]] = abs(self.tversky_measure_identity['AC']-self.tversky_measure_identity[combination[0]+combination[1]])
    #         #     self.identity_difference[combination[0]+combination[1]] += abs(self.tversky_measure_identity['DF']-self.tversky_measure_identity[combination[0]+combination[1]])
    #
    #     print("TVERSKY IDENTITY Difference\n", self.identity_difference)
    #     best_answer = max(self.identity_difference, key=self.identity_difference.get)
    #     unique = sum(value == self.identity_difference[best_answer] for value in self.identity_difference.values())
    #     # while unique != 1:
    #     #     self.identity_difference = {k: v for k, v in self.identity_difference.items() if v != self.identity_difference[best_answer]}
    #     #     best_answer = max(self.identity_difference, key=self.identity_difference.get)
    #     #     unique = sum(value == self.identity_difference[best_answer] for value in self.identity_difference.values())
    #     #     #minimum_value = second_minimum_value
    #
    #
    #     if unique==1:
    #         best_answer = best_answer
    #         return int(best_answer)
    #     #print(problem.name)
    #     #print("Flag")
    #     #self.problem_name = problem.name
    #     #folder_name = 'Problems/{}s {}/{}/'.format(problem.name.rsplit(' ', 1)[0], problem.name.split('-')[0].rsplit(' ', 1)[1], problem.name)
    #     #for figure_name in self.figure_names:
    #     #    print("Figure Name: ", figure_name)
    #     #    self.figure_pixel_matrix[figure_name] = self.open_image_return_pixels(Image.open('{}{}.png'.format(folder_name, figure_name)).convert('1'))
    #     for combination in [['A', 'C'], ['D', 'F'], ['A', 'G'], ['B', 'H'], ['G', 'C'], ['G', '1'] , ['G', '2'], ['G', '3'], ['G', '4'], ['G', '5'], ['G', '6'], ['G', '7'], ['G', '8'], ['C', '1'] , ['C', '2'], ['C', '3'], ['C', '4'], ['C', '5'], ['C', '6'], ['C', '7'], ['C', '8'], ['A', '1'] , ['A', '2'], ['A', '3'], ['A', '4'], ['A', '5'], ['A', '6'], ['A', '7'], ['A', '8']]:
    #         # print("combination : ", combination)
    #         # print("Combination[0]:", combination[0])
    #         # print("Combination[1]:", combination[1])
    #
    #         #self.tversky_measure[combination[0] + combination[1]] = self.tversky_score(self.figure_pixel_2d[combination[0]], self.crop_reflect_merge(self.figure_pixel_2d[combination[1]]))
    #         self.tversky_measure[combination[0] + combination[1]] = self.tversky_score(self.figure_pixel_2d[combination[0]], self.crop_reflect_merge(self.figure_pixel_2d[combination[1]]))
    #
    #
    #         # print("figure_similarity[combination[0] + combination[1]]:", self.figure_similarity[combination[0] + combination[1]])
    #         # print("Combination [0], [1] :", combination[0], combination[1])
    #
    #     #horizontal = self.tversky_measure['AC'] - self.tversky_measure['DF']
    #     #vertical = self.tversky_measure['AG'] - self.tversky_measure['BH']
    #     print("OPTION_SCORE_0\n", self.option_score)
    #     for option in [ ['G', '1'] , ['G', '2'], ['G', '3'], ['G', '4'], ['G', '5'], ['G', '6'], ['G', '7'], ['G', '8'], ['C', '1'] , ['C', '2'], ['C', '3'], ['C', '4'], ['C', '5'], ['C', '6'], ['C', '7'], ['C', '8'], ['A', '1'] , ['A', '2'], ['A', '3'], ['A', '4'], ['A', '5'], ['A', '6'], ['A', '7'], ['A', '8']]: #['H','1'], ['H','2'], ['H','3'], ['H','4'], ['H','5'], ['H','6'], ['H','7'], ['H','8']]:
    #         threshold = 0.005
    #         if option[0] == 'G':
    #             #start checking similarity between AC, DF and option[0]+option[1]
    #             if (abs(self.tversky_measure['AC']-self.tversky_measure[option[0]+option[1]])<0.001):
    #                 self.option_score[option[1]] += abs(self.tversky_measure['AC']-self.tversky_measure[option[0]+option[1]])
    #
    #             if (abs(self.tversky_measure['DF']-self.tversky_measure[option[0]+option[1]])<0.001):
    #                 self.option_score[option[1]] += abs(self.tversky_measure['DF']-self.tversky_measure[option[0]+option[1]])
    #
    #         if option[0] == 'C':
    #             #start checking similarity between AC, DF and option[0]+option[1]
    #             if (abs(self.tversky_measure['AG']-self.tversky_measure[option[0]+option[1]])<0.001):
    #                 self.option_score[option[1]] += abs(self.tversky_measure['AG']-self.tversky_measure[option[0]+option[1]])
    #
    #             if(abs(self.tversky_measure['BH']-self.tversky_measure[option[0]+option[1]])<0.001):
    #                 self.option_score[option[1]] += abs(self.tversky_measure['BH']-self.tversky_measure[option[0]+option[1]])
    #
    #         if option[0] == 'A':
    #             #start checking similarity between AC, DF and option[0]+option[1]
    #             if (abs(self.tversky_measure['GC']-self.tversky_measure[option[0]+option[1]])<0.001):
    #                 self.option_score[option[1]] += abs(self.tversky_measure['GC']-self.tversky_measure[option[0]+option[1]])
    #         #
    #         # if option[0] == 'H':
    #         #     if (abs(self.tversky_measure_identity['BC']-self.tversky_measure_identity[option[0]+option[1]])<0.001):
    #         #         self.option_score[option[1]] += abs(self.tversky_measure['BC']-self.tversky_measure[option[0]+option[1]])
    #
    #
    #
    #     #print("OPTION_SCORE\n", self.option_score)
    #     max_key = max(self.option_score, key=self.option_score.get)
    #     best_answer = max_key
    #     unique = sum(value == self.option_score[best_answer] for value in self.option_score.values())
    #
    #     if(unique == 1):
    #         return int(best_answer)
    #     else:
    #         return -1

    # def xor_check(self):
    #     best_answer = 1
    #     self.figure_objects = {}
    #     self.tversky_measure_identity = {}
    #     self.option_score = {}
    #
    #     for combination in [['A', 'B'], ['B', 'C'], ['G', 'H'], ['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'],
    #                         ['H', '5'], ['H', '6'], ['H', '7'], ['H', '8'], ['D', 'E'], ['E', 'F'], ['A', 'D'],
    #                         ['D', 'G'], ['C', 'F'], ['F', '1'], ['F', '2'], ['F', '3'], ['F', '4'],['F', '5'],
    #                         ['F', '6'], ['F', '7'], ['F', '8']]:
    #         self.xor_measure[combination[0] + combination[1]] = self.xor(self.figure_pixel_2d[combination[0]], self.figure_pixel_2d[combination[1]])
    #
    #     #print("XOR_SCORES\n", self.xor_measure)
    #
    #     test = (1-abs((self.xor_measure['AB']/self.xor_measure['BC'])-(self.xor_measure['DE']/self.xor_measure['EF'])))
    #     #print("(XOR_AB/XOR_BC): ", self.xor_measure['AB']/self.xor_measure['BC'])
    #     #print("(XOR_DE/XOR_EF): ", self.xor_measure['DE']/self.xor_measure['EF'])
    #     #print("(1-abs((XOR_AB/XOR_BC)-(XOR_DE/XOR_EF)))\n", test)
    #
    #     for combination in [['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'],['H', '5'],
    #                         ['H', '6'], ['H', '7'], ['H', '8']]:
    #         self.option_score[combination[0] + combination[1]] = (1-abs((self.xor_measure['AB']/self.xor_measure['BC'])-(self.xor_measure['GH']/self.xor_measure[combination[0]+combination[1]])))
    #
    #     for combination in [['F', '1'], ['F', '2'], ['F', '3'], ['F', '4'],['F', '5'],
    #                         ['F', '6'], ['F', '7'], ['F', '8']]:
    #         self.option_score[combination[0] + combination[1]] = (1-abs((self.xor_measure['AD']/self.xor_measure['DG'])-(self.xor_measure['CF']/self.xor_measure[combination[0]+combination[1]])))
    #
    #     print(self.option_score)
    #     best_answer = max(self.option_score, key=self.option_score.get)
    #     print("best answer\n", best_answer)
    #     second_best_answer = dict(sorted(self.option_score.items(), key=lambda item: item[1]))
    #     second_best_key = list(second_best_answer)[-2]
    #     second_best_value = list(second_best_answer.values())[-2]
    #     print(f"Second Best Key: {second_best_key}, Second Best Value: {second_best_value}")
    #     #print("second best answer\n", second_best_answer)
    #     if best_answer[1] == second_best_key[1] and self.option_score[best_answer]>0.98: # and abs(self.option_score[best_answer]-second_best_value) > 0.05:
    #         return int(best_answer[1])
    #     else:
    #         return -1
    #
    #
    # def xor(self, temp1, temp2):
    #     answer = 0
    #     c1 = 0
    #     c2 = 0
    #     for i in range(temp1.shape[0]):
    #         for j in range(temp1.shape[1]):
    #             if temp1[i, j] == 0:
    #                 c1 += 1
    #             if temp2[i, j] == 0:
    #                 c2 += 1
    #
    #
    #     # for i in range(temp1.shape[0]):
    #     #     for j in range(temp1.shape[1]):
    #     #         if temp1[i, j] == 0 and temp2[i, j] == 0:
    #     #             answer+="0"
    #     #         elif temp1[i, j] == 0 and temp2[i, j] == 255:
    #     #             answer+="1"
    #     #         elif temp1[i, j] == 255 and temp2[i, j] == 0:
    #     #             answer += "1"
    #
    #     #answer = np.reshape(np.array(answer), (temp1.shape[0], temp1.shape[1]))
    #     #print(len(answer))
    #     #answer = int(answer, 2)
    #     if c2 == 0:
    #         return 1
    #     answer = c1/c2
    #     return answer





# ---------------------------Not Updated DELETE!!!---------------------
    # def method_unchanged(self):
    #     flag = 1
    #     best_answer = -1
    #     similarity_maximum = 0
    #     for combination in [['A', 'B'], ['B', 'C'], ['D', 'E'], ['E', 'F'], ['G', 'H']]:
    #         if self.figure_similarity[combination[0] + combination[1]] < 98:
    #             flag = 0
    #     if flag == 1:
    #         for combination in [['H', '1'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'], ['H', '6'], ['H', '7'], ['H', '8']]:
    #             this_similarity = self.figure_similarity[combination[0] + combination[1]]
    #             if this_similarity > similarity_maximum:
    #                 best_answer = combination[1]
    #                 similarity_maximum = this_similarity
    #     return best_answer

    def fill_hollow_shape(self):
        union = {}

        for combination in [["A", "B"], ["A", "C"]]:
            union[combination[0] + combination[1]] = self.union(self.figure_pixel_2d[combination[0]],
                                                                self.figure_pixel_2d[combination[1]])


        union["AB"] = self.union(self.figure_pixel_2d["A"], self.figure_pixel_2d["B"])
        union["AC"] = self.union(self.figure_pixel_2d["A"], self.figure_pixel_2d["C"])



        max = 0
        best_answer = "-1"
        bothAB = 0
        bothAC = 0

        black_pixel_ab = self.black_pixel_counter(union["AB"])
        black_pixel_b = self.black_pixel_counter(self.figure_pixel_2d["B"])

        print(black_pixel_ab - black_pixel_b)
        #print(black_pixel_b)

        for k in range(184):
            for l in range(184):
                if union["AB"][k, l] == self.figure_pixel_2d["B"][k, l]:
                    bothAB += 1
                if union["AC"][k, l] == self.figure_pixel_2d["C"][k, l]:
                    bothAC += 1
        print("BOTHAB UNION: ", bothAB)
        if bothAB > 32000:
            # print("BOTHAB UNION: ", bothAB)
            for option in self.options:
                union["C" + option] = self.union(self.figure_pixel_2d["C"], self.figure_pixel_2d[option])
                both = 0
                for i in range(184):
                    for j in range(184):
                        if union["C" + option][i, j] == self.figure_pixel_2d[option][i, j]:
                            both += 1
                if both > max and both > 33000:
                    max = both
                    best_answer = option
            return int(best_answer)

    # noinspection PyPep8Naming
    def Solve(self, problem: RavensProblem):
        #if 'B-' in problem.name or 'C-' in problem.name or 'Challenge' in problem.name:
        if 'C-' in problem.name or 'D-' in problem.name or 'E-' in problem.name or 'Challenge' in problem.name:
             return -1
        self.initialize_2x2(problem)
        #for possible_method in [self.matching_combination]:

        for possible_method in [self.all_same, self.solve_by_mirror, self.solve_by_union_of_two, self.matching_combination, self.method_vertical_flip, self.fill_hollow_shape]: # self.solve_by_union_of_three]: # self.method_unchanged, self.parse_objects_in_figures, self.method_xor_two_to_get_third, self.method_and_two_to_get_third, self.method_merge_two_to_get_third, self.method_simple_iterate, self.method_merge_row, self.method_change_of_area_to_get_third, self.method_simpler_change_of_area_to_get_third, self.method_special_case_in_change_of_area, self.method_ugly_number_of_objects]:
            possible_answer = possible_method()
            if possible_answer != -1:
                print("    ", possible_method.__name__)
                print("     Answer: ", possible_answer)
                return possible_answer
        return -1

