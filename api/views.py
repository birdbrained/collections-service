from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request):
    """
    # OSF Collections API Root
    Welcome to the browsable API for OSF Collections. Learn more about each of
    the endponts by clicking on their URL in the response below.
    """

    return Response({

        'collections': reverse('collection-list', request=request),
        'items': reverse('item-list', request=request),
        'documents': reverse('document-list', request=request),
        'collection-memberships': reverse('collectionmembership-list', request=request),
        'schemas': reverse('schema-list', request=request),
        'workflows': reverse('workflow-list', request=request),
        'cases': reverse('case-list', request=request),
        'widgets': reverse('widget-list', request=request),
        'parameters': reverse('parameter-list', request=request),
        'parameter-stubs': reverse('parameterstub-list', request=request),
        'parameter-aliases': reverse('parameteralias-list', request=request),
        'sections': reverse('section-list', request=request)
    })

