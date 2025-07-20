pipeline {
	agent any

	options {
		ansiColor('xterm')
		disableConcurrentBuilds()
	}

	stages {
		stage('Checkout'){
			steps {
				checkout scm
			}
		}
		stage('Sync github repo') {
				when { branch 'master' }
				steps {
						syncRemoteBranch('git@github.com:nbr23/python-fitparse.git', 'master')
				}
		}

	}
}
