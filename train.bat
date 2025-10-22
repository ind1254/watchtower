# Watchtower Train Script
@echo off
echo 🤖 Training fraud detection model...
python -m watchtower.models.train_detector
echo ✅ Model training complete!
