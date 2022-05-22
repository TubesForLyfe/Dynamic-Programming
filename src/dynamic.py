# INITIALIZE
jumlah_matkul = int(input("Masukkan jumlah mata kuliah: "))
max_prediksi = int(input("Masukkan jumlah maksimal prediksi nilai untuk satu mata kuliah: "))
print()
matkul = [[0 for j in range(3)] for i in range(jumlah_matkul)]
for i in range(jumlah_matkul):
    matkul[i][1] = []
    for j in range(max_prediksi + 1):
        matkul[i][1].append([0, 0])

# INPUT
for i in range(jumlah_matkul):
    print("Masukkan nama mata kuliah ke-" + str(i+1), end="")
    matkul[i][0] = input(": ")
    print()
    input_prediksi = 'y'
    count_prediksi = 0
    while (input_prediksi == 'y' and count_prediksi < max_prediksi):
        print("Masukkan prediksi jam belajar untuk mata kuliah", matkul[i][0], end="")
        matkul[i][1][count_prediksi + 1][0] = int(input(": "))
        print("Masukkan prediksi nilai untuk", matkul[i][1][count_prediksi + 1][0], "jam belajar mata kuliah", matkul[i][0], end="")
        matkul[i][1][count_prediksi + 1][1] = int(input(": "))
        count_prediksi += 1
        if (count_prediksi != max_prediksi):
            input_prediksi = input("Ingin memasukkan prediksi lagi? (y/n): ")
        print()
    matkul[i][2] = count_prediksi
    for j in range(count_prediksi, max_prediksi):
        matkul[i][1][j + 1][0] = '-'
        matkul[i][1][j + 1][1] = '-'

# OUTPUT FROM INPUT
print("Berikut merupakan prediksi keseluruhan mata kuliah Anda:")
for i in range(jumlah_matkul):
    print(matkul[i][0])
    for j in range(matkul[i][2]):
        print("\tPrediksi " + str(j + 1) + ":")
        print("\t\tJam belajar:", matkul[i][1][j + 1][0])
        print("\t\tNilai:", matkul[i][1][j + 1][1])
print()

# REQUIRED FUNCTION
def getOptimal(array):
    idx = 0
    result = array[idx]
    for i in range(1, len(array)):
        if (array[i] != '-'):
            if (array[i] > result):
                idx = i
                result = array[i]
    idx_result = []
    for i in range(len(array)):
        if (array[i] == result):
            idx_result.append(i)
    return [result, idx_result]

def getSolution(idx_matkul, matkul, optimal, hour_cost):
    solution = []
    if (idx_matkul >= 0):
        for i in range(len(optimal[idx_matkul][hour_cost][1])):
            solution.append(optimal[idx_matkul][hour_cost][1][i])
            solution.append(getSolution(idx_matkul - 1, matkul, optimal, hour_cost - matkul[idx_matkul][1][optimal[idx_matkul][hour_cost][1][i]][0]))
    return solution

def getFirstSolution(arr):
    solution = []
    while (len(arr) != 0):
        solution.append(arr[0])
        arr = arr[1]
    for i in range(len(solution)//2):
        temp = solution[i]
        solution[i] = solution[len(solution) - i - 1]
        solution[len(solution) - i - 1] = temp
    return solution

# DYNAMIC PROGRAMMING PROCESS
MAX_HOUR = int(input("Jam belajar maksimal yang Anda miliki: "))
tahap = [0 for i in range(jumlah_matkul)]
optimal = [0 for i in range(jumlah_matkul)]
for i in range(jumlah_matkul):
    tahap[i] = [0 for j in range(MAX_HOUR + 1)]
    optimal[i] = [0 for j in range(MAX_HOUR + 1)]
    for j in range(MAX_HOUR + 1):
        tahap[i][j] = [0 for k in range(matkul[i][2] + 1)]
        optimal[i][j] = [0 for k in range(2)]
        for k in range(matkul[i][2] + 1):
            if (j >= matkul[i][1][k][0]):
                tahap[i][j][k] = matkul[i][1][k][1] # basis
                if (i != 0):
                    tahap[i][j][k] += optimal[i - 1][j - matkul[i][1][k][0]][0] # rekurens
            else:
                tahap[i][j][k] = '-'
        optimal[i][j][0] = getOptimal(tahap[i][j])[0]
        optimal[i][j][1] = getOptimal(tahap[i][j])[1]

# SOLUTION
solution = getFirstSolution(getSolution(jumlah_matkul - 1, matkul, optimal, MAX_HOUR))

# OUTPUT FROM SOLUTION
print("\nSOLUSI:")
count = 0
for i in range(jumlah_matkul):
    if (solution[i] != 0):
        print(str(count + 1) + ". " + matkul[i][0] + ": " + str(matkul[i][1][solution[i]][0]) + " jam belajar => " + str(matkul[i][1][solution[i]][1]))
    count += 1