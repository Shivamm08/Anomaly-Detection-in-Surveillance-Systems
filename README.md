# Anomaly-Detection-in-Surveillance-Systems

This project is one part of my final year project based on Anomaly Detection in Surveillance Systems. This specific part focuses on violence detection, where videos and real-time streams are analyzed to classify scenes as either violent or non-violent. The system leverages deep learning models to accurately detect and highlight violent incidents in surveillance footage.

The model architecture integrates MobileNetV2 as a feature extraction backbone combined with a Bi-LSTM layer for temporal sequence analysis. This combination allows the system to efficiently process both spatial and temporal information from video frames. The system achieves high accuracy in distinguishing violent and non-violent scenarios, with a focus on scalability and real-time performance.

The system also includes a Django-based web interface, which provides an intuitive platform for users to upload videos for analysis or monitor real-time violence detection using a webcam feed. Detected incidents are stored in a database for further review, enabling comprehensive surveillance management.

This project demonstrates the practical application of deep learning in surveillance systems, offering an automated approach to anomaly detection with the potential to enhance public safety and security monitoring systems.
