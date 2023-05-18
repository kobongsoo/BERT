# 클러스터링
- 군집분석(clustering)이란 개체들을 분류(classification)하기 위한 기준이 없는 상태에서 주어진 데이터의 속성값들을 고려해 유사한 개체끼리 그룹(클러스터)화하는 방법이다. 그룹내 차이를 줄이고 그룹간 차이는 최대화 하도록 하여 대표성을 찾는 원리로 구현되는 것이 일반적이다.
즉, 비지도 학습(Unsupervised Learning)에 해당된다.

## 1. K-mean clustering
- K-means는 중심기반(Center-based) 클러스터링 방법으로 “유사한 데이터는 중심점(centroid)을 기반으로 분포할 것이다”는 가정을 기반으로 한다.

![image](https://github.com/kobongsoo/BERT/assets/93692701/e274d306-72ed-4ebd-a4de-3ab5d5c3a03c)

1. 초기점(k) 설정
k는 중심점(centroid)이자, 묶일 그룹(cluster)의 수와 같다.
위 예시에서는 k=3으로 설정(동그라미)

2. 그룹(cluster) 부여
k개의 중심점(동그라미)과 개별 데이터(네모)간의 거리를 측정한다.
가장 가까운 중심점으로 데이터를 부여한다.

3. 중심점(centroid) 업데이트
할당된 데이터들의 평균값(mean)으로 새로운 중심점(centroid)을 업데이트한다.

4. 최적화
2,3번 작업을 반복적으로 수행한다.
변화가 없으면 작업을 중단한다.

#### *출처 : https://brilliant.org/wiki/k-means-clustering/

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[K-Mean-test-1](https://github.com/kobongsoo/BERT/blob/master/clustering/K-Means-test-1.ipynb)|K-Mean 예제1||
|[K-Mean-test-2](https://github.com/kobongsoo/BERT/blob/master/clustering/K-Means-test-2.ipynb)|K-Mean 예제2||

## 2. DBSCAN clustering
- DBSCAN는 밀도기반(Density-based) 클러스터링 방법으로 “유사한 데이터는 서로 근접하게 분포할 것이다”는 가정을 기반으로 한다. K-means와 달리 처음에 그룹의 수(k)를 설정하지 않고 자동적으로 최적의 그룹 수를 찾아나간다.

![image](https://github.com/kobongsoo/BERT/assets/93692701/5223b963-5784-4942-a565-6b9f52877dfb)

1. 먼저 하나의 점(파란색)을 중심으로 반경(eps) 내에 최소 점이 4개(minPts=4)이상 있으면, 하나의 군집으로 판단하며 해당 점(파란색)은 Core가 된다.
2. 반경 내에 점이 3개 뿐이므로 Core가 되진 않지만 Core1의 군집에 포함된 점으로, 이는 Border가 된다.
3. 1번과 마찬가지로 Core가 된다.
4. 그런데 반경내의 점중에 Core1이 포함되어 있어 군집을 연결하여 하나의 군집으로 묶인다.

#### * 출처 : https://yganalyst.github.io/ml/ML_clustering/

## 3. HDBSCAN clustering
- HDBSCAN 은 이전 모델과 달리 다양한 밀도의 클러스터를 식별할 수 있는 DBSCAN을 기반으로 구축 된 보다 최근에 개발된 알고리즘. 
- 알고리즘은 각 데이터 포인트의 코어 거리를 찾는데,  eps를 해당 덴드로그램의 컷오프로 사용하는 DBSCAN과 달리 HDBSCAN은 클러스터에서 떨어지는 포인트로 분리되는 소수의 포인트만 생성하는 분할을 확인 한다.
- 그 결과 포인트를 잃는 클러스터 수가 적은 더 작은 트리가 생성되며 가장 안정적이고 지속적인 클러스터를 선택하는 데 사용할 수 있다.

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[HDBSCAN-test-1](https://github.com/kobongsoo/BERT/blob/master/clustering/HDBSCAN-test-1.ipynb)|HDBSCAN 예제1||
|[HDBSCAN-test-2](https://github.com/kobongsoo/BERT/blob/master/clustering/HDBSCAN-test-2.ipynb)|HDBSCAN 예제2||
