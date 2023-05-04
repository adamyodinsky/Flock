package controllers

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/adamyodinsky/Flock/flock_deployer/models"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	appsv1 "k8s.io/client-go/kubernetes/typed/apps/v1"
	corev1 "k8s.io/client-go/kubernetes/typed/core/v1"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

func Deploy(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)
	var deployment models.Deployment
	json.Unmarshal(reqBody, &deployment)

	// Set up the Kubernetes client configuration
	config, err := rest.InClusterConfig()
	if err != nil {
		// Fallback to using kubeconfig if in-cluster config is not available
		config, err = clientcmd.BuildConfigFromFlags("", "/path/to/your/kubeconfig")
		if err != nil {
			panic(err.Error())
		}
	}

	// Create a Kubernetes clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err.Error())
	}

	// Create the Deployment
	err = createDeployment(clientset.AppsV1(), deployment)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(deployment)
}

func createDeployment(client appsv1.AppsV1Interface, d models.Deployment) error {
	// Define the desired Deployment resource
	deployment := &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      d.Metadata.Name,
			Namespace: d.Namespace,
			Labels:    d.Metadata.Labels,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: int32Ptr(1),
			Selector: &metav1.LabelSelector{
				MatchLabels: d.Metadata.Labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: d.Metadata.Labels,
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  d.Metadata.Name,
							Image: "your-image-here",
							Ports: []corev1.ContainerPort{
								{
									ContainerPort: int32(8080),
									Protocol:      corev1.ProtocolTCP,
								},
							},
						},
					},
				},
			},
		},
	}

	// Check if the Deployment already exists
	_, err := client.Deployments(d.Namespace).Get(context.Background(), d.Metadata.Name, metav1.GetOptions{})
	if errors.IsNotFound(err) {
		// Create the Deployment
		_, err = client.Deployments(d.Namespace).Create(context.Background(), deployment, metav1.CreateOptions{})
		if err != nil {
			return fmt.Errorf("failed to create deployment: %v", err)
		}
	} else if err != nil {
		return fmt.Errorf("failed to get deployment: %v", err)
	} else {
		// Deployment already exists
		return fmt.Errorf("deployment already exists")
	}

	return nil
}

// Helper function to create a pointer to an int32 value
func int32Ptr(i int32) *int32 {
	return &i
}
