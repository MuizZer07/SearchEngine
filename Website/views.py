from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .form import searchForm
from .json_reader import Json_Reader
from .Products import Product
from .firebase_loader import firebase_loader

class HomeView(TemplateView):
    template_name = 'webs/index.html'

    def get(self, request):
        form = searchForm()

        args = {
                'form': form
            }

        return render(request, self.template_name, args)

    def post(self, request):
        form = searchForm(request.POST)
        json = Json_Reader()
        products = []

        data = json.read_file()

        if form.is_valid():
            text = form.cleaned_data['Search']
            
        for product in data:
            title = product['title']
            if text.lower() in title.lower():
                title = product['title']
                asin = product['asin']
                brand = product['brand']
                feature = product['feature']
                price = product['price']
                image = product['images']
                categories = product['categories']
                product = Product(asin, title, brand, feature, price, image, categories)
                products.append(product)
        args = {
            'form': form,
            'text': text,
            'data': data, 
            'products': products,
        }

        return render(request, self.template_name, args)