from flask import Flask, render_template, request, jsonify
from .obsidian_helper import load_config
from .scripts import ai_assistant, productivity_analysis, knowledge_graph, realtime_collaboration, ai_insights

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance_note', methods=['POST'])
def enhance_note():
    note_path = request.json['note_path']
    enhanced_note = ai_assistant.enhance_note(note_path)
    return jsonify({'enhanced_note': enhanced_note})

@app.route('/analyze_productivity')
def analyze_productivity():
    config = load_config()
    output_path = productivity_analysis.analyze_productivity(config)
    return jsonify({'productivity_analysis': output_path})

@app.route('/generate_knowledge_graph')
def generate_graph():
    config = load_config()
    graph_path = knowledge_graph.generate_knowledge_graph(config)
    return jsonify({'knowledge_graph': graph_path})

@app.route('/start_collaboration')
def start_collaboration():
    config = load_config()
    collaboration = realtime_collaboration.RealtimeCollaboration(config)
    collaboration.start_server()
    return jsonify({'message': 'Collaboration server started'})

@app.route('/generate_ai_insights')
def generate_ai_insights():
    config = load_config()
    insight_path = ai_insights.generate_ai_insights(config)
    return jsonify({'ai_insights': insight_path})

def run_web_interface():
    app.run(debug=True)

if __name__ == '__main__':
    run_web_interface()