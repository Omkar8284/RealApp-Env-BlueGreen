pipeline {
  agent any

  environment {
    IMAGE = "omkar8284/realapp"
    KUBECONFIG = credentials('k3s-Kubeconfig')   // your Jenkins secret-file ID
  }

  stages {
    stage('Checkout') {
      steps { git branch: 'main', url: 'https://github.com/Omkar8284/RealApp-Env-BlueGreen.git' }
    }

    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build("${IMAGE}:${BUILD_NUMBER}")
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
            dockerImage.push()
            dockerImage.push('latest')
          }
        }
      }
    }

    stage('Update K8s Deployments (image)') {
      steps {
        script {
          sh """
            # Update both deployments to the new image tag
            kubectl set image deployment/demo-app-blue demo-app=${IMAGE}:${BUILD_NUMBER} --record
            kubectl set image deployment/demo-app-green demo-app=${IMAGE}:${BUILD_NUMBER} --record

            # Wait for both deployments to roll out
            kubectl rollout status deployment/demo-app-blue --timeout=120s
            kubectl rollout status deployment/demo-app-green --timeout=120s
          """
        }
      }
    }

    stage('Traffic Switch (Blue -> Green)') {
      steps {
        script {
          sh '''
            # switch service selector to green
            kubectl patch svc demo-app-service -p '{"spec": {"selector": {"app":"demo-app","role":"green"}}}'
            # verify that endpoints changed
            sleep 3
            kubectl get endpoints demo-app-service -o wide
            # wait and verify a healthy rollout by curling the ingress host
            for i in 1 2 3 4 5; do
              echo "curl attempt $i"
              curl -sSf --retry 3 --retry-delay 2 --max-time 5 http://node2.local/ && break || sleep 2
            done
          '''
        }
      }
    }

    stage('Verify & Optional Rollback') {
      steps {
        script {
          def healthy = sh(script: "curl -sSf http://node2.local/ || echo 'UNHEALTHY'", returnStdout:true).trim()
          if (healthy == 'UNHEALTHY') {
            echo "Health check failed — rolling back to blue"
            sh "kubectl patch svc demo-app-service -p '{\"spec\": {\"selector\": {\"app\":\"demo-app\",\"role\":\"blue\"}}}'"
            error("Deployment failed health check - rolled back")
          } else {
            echo "Health check OK - deployment successful"
          }
        }
      }
    }
  }

  post {
    failure {
      script {
        echo "Build failed. Check Jenkins logs."
      }
    }
    success {
      echo "Pipeline completed successfully."
    }
  }
}

