from .utils import extract_sample 

class Reducer:
    def __init__(self, database, sample_rate=1.0):
        self.database = database              
        self.sample_rate = sample_rate        
        self.sample_path = None               

    def preprocess(self):
        print("🚀 Starting data preprocessing...")
        self.sample_path = extract_sample(self.database, self.sample_rate)
        print(f"✅ Sample file saved at: {self.sample_path}")
