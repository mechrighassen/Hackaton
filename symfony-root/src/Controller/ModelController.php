<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

// Permet d'envoyer des requêtes HTTP à l'API
use Unirest;

class ModelController extends AbstractController
{
	/**
	 * @Route("/model/index", name="model_index")
	 * Page d'accueil du site, affiche l'ensemble des modèles déjà existants
	 */
	public function model_index()
	{
		// Envoie une requête GET à l'API à la route /model
		$response = Unirest\Request::get(
			'http://localhost:5000/model',
			[
				'accept' => 'application/json',
			]
		);

		// On récupère l'ensemble des modèles à partir de la réponse obtenue
		// TODO: Vérifier si la requête s'est bien passée
		$model_ = json_decode($response->raw_body, true);

		// Rendu de la page
		return $this->render('model/model_index.html.twig', [
			'controller_name' => 'ModelController',
			'model_' => $model_,
		]);
	}

	/**
	 * @Route("/model/new", name="model_new")
	 * Renvoit une page avec un formulaire pour créer un nouveau modèle
	 */
	public function model_new()
	{
		return $this->render('model/model_form.html.twig', [
			'controller_name' => 'ModelController',
		]);
	}

	/**
	 * @Route("model/add", name="model_add")
	 * Ajoute effectivement un modèle. Doit être appelée en POST. Cette route
	 * renvoit une redirection vers une route qui affiche le modèle créé.
	 */
	public function model_add(Request $request)
	{
		// Description de ce qui sera envoyé à l'API en POST
		$body = Unirest\Request\Body::json([
				'algorithmes' => $request->get('algorithm'),
				'parameteres' => null,
		]);

		$response = Unirest\Request::post(
			'http://localhost:5000/model/add',
			[
				'Accept' => 'application/json',
				'Content-type' => 'application/json',
			],
			$body
		);

		// TODO: vérifier que la requête s'est bien passée.

		// On récupère l'identifiant du modèle qui vient d'être ajoutée.
		$id = json_decode($response->raw_body, true)['id'];

		// Redirection vers la page créée.
		return $this->redirectToRoute('model_show', [
			'id' => $id,
		]);
	}

	/**
	 * @Route("/model/show/{id}", name="model_show")
	 * Affiche un modèle.
	 */
	public function model_show($id)
	{
		$response = Unirest\Request::get(
			"http://localhost:5000/model/{$id}",
			[
				'Accept' => 'application/json',
			],
		);

		$model = json_decode($response->raw_body, true)[0];

		return $this->render('model/model_show.html.twig', [
			'controller_name' => 'ModelController',
			'model' => $model,
		]);
	}

	/**
	 * @Route("model/delete/{id}", name="model_delete")
	 * Efface une route. Renvoit une redirection vers l'index.
	 */
	public function model_delete($id)
	{
		$response = Unirest\Request::delete(
			"http://localhost:5000/model/{$id}",
			[
				'Accept' => 'application/json',
			],
			[]
		);

		$this->addFlash('success', 'The model has been deleted');
		return $this->redirectToRoute('model_index');
	}
}
