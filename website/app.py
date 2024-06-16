from flask import Flask, render_template, request, redirect, url_for

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
    query = request.args.get('query')
    
    # Here you can process the query and prepare data for the results page
    # Example: Perform a search query or fetch data based on the query
    
    # For demonstration purposes, redirect to a results page with the query in the URL
    return redirect(url_for('show_results', query=query))

# Route to display search results
@app.route('/results/<query>')
def show_results(query):
    # Example: You can fetch results based on the query and pass them to the template
    # Example: results = fetch_results(query)
    
    # For now, let's pass the query to the template
    return render_template('results.html', query=query)

if __name__ == '__main__':
    app.run()

