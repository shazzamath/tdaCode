
from myImports import *
from Classes import PersisMod

def main():
    with open("point_clouds.json", "r") as f:
        json_data = json.load(f)
    point_clouds = {float(key): np.array(value) for key, value in json_data.items()}

    trainset = []
    testset = []
    for lam in point_clouds.keys():
        t = PersisMod(point_clouds[lam],lam)
        if len(testset)< 5:
            testset.append(t)
        else:
            trainset.append(t)

    dist_matrix = [[0 for j in range(len(trainset))] for i in range(len(testset))]
    for i in range(len(testset)):
        for j in range(i,len(trainset)):
            dist = testset[i].distance_to(trainset[j], "bottleneck")
            dist_matrix[i][j], dist_matrix[j][i] = dist, dist
    
    predictions = []
    for t in dist_matrix:
        s = sorted(t)
        summ = 0
        for i in range(0,3):
            loc = t.index(s[i])
            summ += trainset[loc].mapping
        predictions.append(summ/3)

    errors = []
    for i in range(len(testset)):
        diff = testset[i].mapping -  predictions[i]
        error = abs(diff)/testset[i].mapping
        errors.append(error)
    print(errors)

if __name__ == "__main__":
    main()
