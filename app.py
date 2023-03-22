from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
X = pickle.load(open('X.pkl','rb'))
ratings = pickle.load(open('ratings.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           product = list(popular_df['product_id'].values),
                           rating = list(popular_df['rating_x'].values),
                           image = list(popular_df['image_url'].values),
                           price = list(popular_df['price'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_kurtis', methods=['post'] )
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(X.index==user_input)[0][0]
    similar_items= sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)
    
    data = []
    for i in similar_items:
        item = [] 
        temp_df = ratings[ratings['product_id']==X.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('product_id')['product_id'].values))
        item.extend(list(temp_df.drop_duplicates('product_id')['image_url'].values))
        item.extend(list(temp_df.drop_duplicates('product_id')['price'].values))
        
        data.append(item)

        print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)