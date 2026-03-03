import csv
from sklearn.neighbors import KNeighborsClassifier

x=[]
y=[]
dlabels=[]

with open('Crop_recommendation.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    i=0
    for lines in csvFile:
        # print(lines)

        if i!=0:
            r=[]
            for j in range(7):
                r.append(float(lines[j]))
            x.append(r)
            if lines[7] not in dlabels:
                dlabels.append(lines[7])

            y.append(dlabels.index(lines[7]))
        i=i+1
print(x)
print(dlabels)
print(y)

# print(x[0])
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
# print(scaler,"ggggggggggggggggggggggg")
scaler.fit(x)
# print(scaler.fit(x))

# print(scaler.data_max_)

x=scaler.transform(x)
# print(x,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)