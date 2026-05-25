// ============================================================
// Jenkinsfile for CloudTask - Flask Task Manager Application
// Phase 4: Jenkins CI/CD Pipeline
// ============================================================
// This pipeline automates: Test → Build → Deploy
// Triggered manually with "Build Now" in Jenkins
// ============================================================

pipeline {
    agent any    // Run on any available Jenkins agent (your local machine)

    // --------------------------------------------------------
    // Environment Variables
    // Jenkins runs as the Windows Local System account (SYSTEM),
    // whose home is C:\Windows\system32\config\systemprofile.
    // Minikube and kubectl look for configs under the current
    // user's home by default, so SYSTEM cannot find your
    // Minikube cluster or kubeconfig. Setting these two variables
    // tells the tools exactly where to look.
    // --------------------------------------------------------
    environment {
        MINIKUBE_HOME = 'C:\\Users\\thamo\\.minikube'
        KUBECONFIG    = 'C:\\Users\\thamo\\.kube\\config'
    }

    stages {

        // --------------------------------------------------------
        // Stage 1: Checkout
        // Pulls the latest code from your GitHub repository.
        // Jenkins handles this automatically when using "Pipeline from SCM".
        // --------------------------------------------------------
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // --------------------------------------------------------
        // Stage 2: Install Dependencies
        // Installs Python packages listed in requirements.txt.
        // This validates that all dependencies are correct.
        // --------------------------------------------------------
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        // --------------------------------------------------------
        // Stage 3: Test
        // Runs pytest to check that the Flask app works correctly.
        // Tests are in the tests/ folder.
        // --------------------------------------------------------
        stage('Test') {
            steps {
                bat 'python -m pytest tests/ -v'
            }
        }

        // --------------------------------------------------------
        // Stage 4: Build Docker Image
        // Builds a new Docker image from the Dockerfile.
        // Tags it as "cloudtask:latest".
        // --------------------------------------------------------
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t cloudtask:latest .'
            }
        }

        // --------------------------------------------------------
        // Stage 5: Deploy to Kubernetes
        // Loads the image into Minikube, applies K8s manifests,
        // and restarts the deployment to use the new image.
        // --------------------------------------------------------
        stage('Deploy to Kubernetes') {
            steps {
                // Debug: verify Jenkins can see Minikube and the K8s cluster
                bat 'echo MINIKUBE_HOME=%MINIKUBE_HOME%'
                bat 'echo KUBECONFIG=%KUBECONFIG%'
                bat 'minikube status'
                bat 'kubectl config current-context'
                bat 'kubectl get nodes'

                // Load the Docker image into Minikube's internal registry
                bat 'minikube image load cloudtask:latest'

                // Apply Kubernetes manifests (creates resources if they don't exist)
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'

                // Restart the deployment to pick up the new image
                bat 'kubectl rollout restart deployment cloudtask-deployment'

                // Wait for the rollout to finish (max 60 seconds)
                bat 'kubectl rollout status deployment cloudtask-deployment --timeout=60s'
            }
        }
    }

    // --------------------------------------------------------
    // Post-build actions: Run after all stages complete
    // --------------------------------------------------------
    post {
        success {
            echo '✅ Pipeline SUCCESS — CloudTask is deployed to Minikube!'
        }
        failure {
            echo '❌ Pipeline FAILED — Check the stage logs above for errors.'
        }
    }
}
