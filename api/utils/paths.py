import os
from pathlib import Path


class Paths:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        # Data
        current_working_directory = Path.cwd()
        self.dataPath = os.path.join(current_working_directory, 'api/data')
        # self.dataPath = './data'
        # Chat Bot Model
        self._chatBot = f'{self.dataPath}/chatbot_services'
        # Vendor Chat Model
        self._chatVendorService = f'{self._chatBot}/vendor_service'
        self.chatVendorDocs = f'{self._chatVendorService}/docs'
        self.chatVendorIndexing = f'{self._chatVendorService}/indexing'
        self.chatVendorMainIndex = f'{self._chatVendorService}/index'

        # Recommendation Models
        self._recommendationData = f'{self.dataPath}/recommendation'

        # product_similarity_recommendation Model
        self._productsSimilarity = f'{self._recommendationData}/products_similarity'
        self.productsSimilarityTraining = f'{self._productsSimilarity}/train.csv'
        self.productsSimilarityRecommendation = f'{self._productsSimilarity}/recommendation.csv'

        # popularity data
        self._popularity = f'{self._recommendationData}/popularity'
        self.popularityTrain = f'{self._popularity}/train.csv'
        self.popularityRecommendation = f'{self._popularity}/recommendation.csv'

        # collaborative_recommendation_Model
        self._collaborative = f'{self._recommendationData}/collaborative'
        self.collaborativeTraining = f'{self._collaborative}/train.csv'
        self.collaborativeRecommendation = f'{self._collaborative}/recommendation.csv'

        # hybrid_recommendation_Model
        self._hybrid = f'{self._recommendationData}/hybrid'
        self.hybridTraining = f'{self._hybrid}/train.csv'
        self.hybridResults = f'{self._hybrid}/results.csv'

        # image search
        self._imageSearch = f'{self.dataPath}/image_search'
        self.imageSearchTraining = f'{self._imageSearch}/data'
        self.imageSearchFeatures = f'{self._imageSearch}/features.npy'

        # pattern discovery
        self._patternDiscovery = f'{self.dataPath}/pattern_discovery'
        self.patternDiscoveryTraining = f'{self._patternDiscovery}/cart_items.csv'
        self.patternDiscoveryRecommendation = f'{self._patternDiscovery}/rules.csv'



    @property
    def image_search(self):
        return self._imageSearch

mePth = Paths()


# current_working_directory = Path.cwd()
# ff = os.path.join(current_working_directory, 'api/data')
# # Accessing and printing each path
# print(f"Data Path: {mePth.dataPath}")
# print(f"Chat Vendor Docs: {mePth.chatVendorDocs}")
# print(f"Products Similarity Training: {mePth.productsSimilarityTraining}")
# print(f"Popularity Train: {mePth.popularityTrain}")
# print(f"Collaborative Training: {mePth.collaborativeTraining}")
# print(f"Hybrid Training: {mePth.hybridTraining}")
# print(f"Image Search Training: {mePth.imageSearchTraining}")
# print(f"Pattern Discovery Training: {mePth.patternDiscoveryTraining}")
# print(f"Image Search Path (property): {mePth.image_search}")
# print(f"current_working_directory: {current_working_directory}")
# print(f"data path: {ff}")

