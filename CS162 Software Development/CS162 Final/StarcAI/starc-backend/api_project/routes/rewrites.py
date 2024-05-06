# Import necesary libraries.
from flask import Blueprint, jsonify
from api_project.models import Document, TextChunks, Sentence
from api_project import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define the Blueprint for 'rewrite'
rewrite_bp = Blueprint('fix', __name__)

@rewrite_bp.route('/<int:document_id>', methods=['GET'])
@jwt_required()
def get_rewritten_sentences(document_id):
    user_id = get_jwt_identity()

    # Retrieve the document to ensure it belongs to the user
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"message": "Document not found or access denied"}), 404

    # Fetch the text chunk related to the document
    text_chunk = TextChunks.query.filter_by(document_id=document_id).first()
    if not text_chunk:
        return jsonify({"message": "Text chunk not found for the given document"}), 404

    # Fetch and filter the sentences where original and rewritten sentences are different
    sentences = Sentence.query.filter_by(text_chunk_id=text_chunk.id)\
                              .filter(Sentence.original_text != Sentence.rewritten_text)\
                              .all()

    if not sentences:
        return jsonify({"message": "No rewritten sentences found for the given document"}), 404

    # Prepare the response data
    rewritten_sentences_data = [{
        "sentence_id": sentence.id,
        "original_sentence": sentence.original_text,
        "rewritten_sentence": sentence.rewritten_text
    } for sentence in sentences]

    return jsonify(rewritten_sentences_data), 200

@rewrite_bp.route('/<int:document_id>/<int:sentence_id>', methods=['PUT'])
@jwt_required()
def update_sentence(document_id, sentence_id):
    user_id = get_jwt_identity()

    # Validate the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"message": "Document not found or access denied"}), 404

    # Fetch the text chunk and sentence related to the document
    text_chunk = TextChunks.query.filter_by(document_id=document_id).first()
    if not text_chunk:
        return jsonify({"message": "Text chunk not found for the given document"}), 404

    sentence = Sentence.query.filter_by(id=sentence_id, text_chunk_id=text_chunk.id).first()
    if not sentence:
        return jsonify({"message": "Sentence not found"}), 404

    # Update the sentence, this will make it stop showing up as a suggetion.
    if sentence.original_text != sentence.rewritten_text:
        sentence.original_text = sentence.rewritten_text
        db.session.commit()

    # Update the original_text in TextChunks
    updated_sentences = [s.original_text for s in text_chunk.sentences]
    text_chunk.original_text_chunk = " ".join(updated_sentences)
    db.session.commit()

    # Update the word count of the document
    document.word_count = len(text_chunk.original_text_chunk.split())
    db.session.commit()

    return jsonify({"message": "Sentence and document updated successfully"}), 200

@rewrite_bp.route('/<int:document_id>/<int:sentence_id>', methods=['DELETE'])
@jwt_required()
def reset_sentence_to_original(document_id, sentence_id):
    user_id = get_jwt_identity()

    # Validate the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"message": "Document not found or access denied"}), 404

    # Fetch the text chunk and sentence related to the document
    text_chunk = TextChunks.query.filter_by(document_id=document_id).first()
    if not text_chunk:
        return jsonify({"message": "Text chunk not found for the given document"}), 404

    sentence = Sentence.query.filter_by(id=sentence_id, text_chunk_id=text_chunk.id).first()
    if not sentence:
        return jsonify({"message": "Sentence not found"}), 404

    # Update the rewritten text to match the original text
    sentence.rewritten_text = sentence.original_text
    db.session.commit()

    return jsonify({"message": "Sentence reset to original text successfully"}), 200

@rewrite_bp.route('/<int:document_id>/all', methods=['PUT'])
@jwt_required()
def accept_all_suggestions(document_id):
    user_id = get_jwt_identity()

    # Validate the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"message": "Document not found or access denied"}), 404

    # Fetch the text chunk related to the document
    text_chunk = TextChunks.query.filter_by(document_id=document_id).first()
    if not text_chunk:
        return jsonify({"message": "Text chunk not found for the given document"}), 404

    # Update all sentences
    for sentence in text_chunk.sentences:
        sentence.original_text = sentence.rewritten_text
    db.session.commit()

    # Update the original text in TextChunks
    updated_sentences = [s.original_text for s in text_chunk.sentences]
    text_chunk.original_text_chunk = " ".join(updated_sentences)
    db.session.commit()

    # Update the word count of the document
    document.word_count = len(text_chunk.original_text_chunk.split())
    db.session.commit()

    return jsonify({"message": "All suggestions accepted successfully"}), 200

@rewrite_bp.route('/<int:document_id>/all', methods=['DELETE'])
@jwt_required()
def delete_all_suggestions(document_id):
    user_id = get_jwt_identity()

    # Validate the document
    document = Document.query.filter_by(id=document_id, user_id=user_id).first()
    if not document:
        return jsonify({"message": "Document not found or access denied"}), 404

    # Fetch the text chunk related to the document
    text_chunk = TextChunks.query.filter_by(document_id=document_id).first()
    if not text_chunk:
        return jsonify({"message": "Text chunk not found for the given document"}), 404

    # Reset rewritten text for all sentences
    for sentence in text_chunk.sentences:
        sentence.rewritten_text = sentence.original_text
    db.session.commit()

    return jsonify({"message": "All suggestions deleted successfully"}), 200
