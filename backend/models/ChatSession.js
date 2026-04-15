'use strict';

const mongoose = require('mongoose');

const chatSessionSchema = new mongoose.Schema({
    userId: {
        type: String,
        required: true
    },
    disease: {
        type: String,
        required: true
    },
    queries: [{
        question: {
            type: String,
            required: true
        },
        answer: {
            type: String,
            required: true
        },
        sources: {
            type: [String],
            default: []
        },
        clinicalTrials: {
            type: [String],
            default: []
        },
        timestamp: {
            type: Date,
            default: Date.now
        }
    }]
}, { timestamps: true });

module.exports = mongoose.model('ChatSession', chatSessionSchema);
