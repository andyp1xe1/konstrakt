from flask import Flask, render_template, request, redirect, url_for
from retreiver import retreiver, chat
# from img_get import img_get

app = Flask(__name__)


# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/github')
def github():
    return redirect('https://github.com/andyp1xe1/shopping_buddy')


@app.route('/hackathon')
def hackathon():
    return redirect('https://utm.md/en/blog/2024/06/06/fafxsigmoid-summer-hackathon-promises-a-hot-summer/')


# Route to handle search form submission
@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query').lower()

    # Here you can process the query and prepare data for the results page
    # Example: Perform a search query or fetch data based on the query

    # For demonstration purposes, redirect to a results page with the query in the URL
    return redirect(url_for('show_results', query=query))


# Route to display search results
cache = {}


@app.route('/results/<query>')
def show_results(query):
    # Check if the query result is in the cache
    if query in cache:
        resp = cache[query]
        print("Retrieved from cache:", resp)
    else:
        # If not in cache, retrieve and store in cache
        resp = retreiver(query)
        cache[query] = resp
        print("Retrieved from retriever and cached:", resp)

    return render_template('results.html', query=query, resp=resp, )


if __name__ == '__main__':
    app.run()
