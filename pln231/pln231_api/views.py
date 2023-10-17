from django.shortcuts import render

import json 

# Create your views here.

from django.http import JsonResponse 
import openai 
  
openai.api_key = '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'
  
def get_completion(prompt): 
    print(prompt) 
    query = openai.Completion.create( 
        engine="text-davinci-003", 
        prompt=prompt, 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.5, 
    ) 
  
    response = query.choices[0].text 
    print(response) 
    return response 
  
  
def query_view(request): 
    if request.method == 'POST': 
        tipo = request.POST.get('tipo')
        tempo = request.POST.get('tempo')
        ingr = request.POST.get('ingr')
        response = get_completion(gen_prompt(tipo, tempo, ingr))
        print(response)
        response_dict = json.loads(response)
        #return JsonResponse({'response': response})
        return JsonResponse(response_dict, safe=False)
    return render(request, 'index.html')

def gen_prompt(tipo, tempo, ingr):
    return "Preciso de receita tipica do Nordeste brasileiro. \
            Formate a resposta como um JSON com atributos title,\
            description, prep_time, cook_time, ingredients, directions.\
            O tipo de receita esta entre os delimitadores abaixo \
            tipo de receita: ```" + tipo +"```.\
            O tempo de preparo da receita deve ser proximo do que esta entre os delimitadores a seguir\
            tempo medio de preparo: ```" + tempo + "```\
            A receita deve usar alguns dos ingredientes delimitados a seguir\
            ingredientes: ```" + ingr + "```.\
            Se nao gerar receitas, retorne um JSON com os campos vazios."
