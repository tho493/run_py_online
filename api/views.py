import subprocess

from django.http import JsonResponse
from rest_framework import status
# from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .serializers import *
from .admin import *
from rest_framework.parsers import JSONParser
from django.core.exceptions import ObjectDoesNotExist
import json

class run_code(ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        input_data = None
        if('code' not in request.data):
            return JsonResponse({'output': "No code provided", 'error': True}, status=status.HTTP_204_NO_CONTENT)
        return self.run(request.data['code'], input_data)
        
        
    def run(self, code, input_data, timeout=None, *args, **kwargs):
        try:
            process = subprocess.Popen(['python', '-c', code],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            stdout, stderr = process.communicate(input=input_data, timeout=timeout)
            if process.returncode == 0:
                return JsonResponse({'output': stdout, 'error': None}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'output': None, 'error': stderr}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'output': None, 'error': str(e)}, status=status.HTTP_200_OK)


"""
{
    "test_part": {
        "name": "Test Part 1",
        "description": "Description for Test Part 1"
    },
    "test_cases": [
        {
            "output": "pass",
            "variables": [
                {"var": "variable1", "input": "value1"},
                {"var": "variable2", "input": "value2"}
            ]
        },
        {
            "output": "fail",
            "variables": [
                {"var": "variable3", "input": "value3"}
            ]
        }
    ]
}
"""
class add_test_case(ListCreateAPIView):
    queryset = test_part.objects.all().order_by('id')
    serializer_class = TestPartSerializer
    parser_classes = [JSONParser]

    def create(self, request):
        data = request.data
        test_part_data = data.get('test_part', {})
        test_cases_data = data.get('test_cases', [])

        # return JsonResponse({'error': None, 'message': test_part_data}, status=status.HTTP_200_OK)

        if not test_part_data or not test_cases_data:
            return JsonResponse({'error': 'Missing required fields', 'message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

        test_part_create_new = test_part.objects.create(**test_part_data)

        if not test_part_create_new:
            return JsonResponse({'error': 'Failed to create test part', 'message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

        for testcase_data in test_cases_data:
            output = {'output':testcase_data.get('output', {})}
            test_case_create_new = test_case.objects.create(test_part=test_part_create_new, **output)

            for variable_data in testcase_data.get('variables', []):
                variable.objects.create(test_case=test_case_create_new, **variable_data)

        return JsonResponse({'message': 'Test part and test cases added successfully'}, status=status.HTTP_200_OK)

class delete_test_case(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            test_part_instance = test_part.objects.get(id=request.data.get('test_part_id'))
            test_part_instance.delete()
            return JsonResponse({'error': None, 'message': 'Test part deleted'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No matching test part found', 'message': 'failed'}, status=status.HTTP_404_NOT_FOUND)
    
class update_test_case(ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        

        return JsonResponse({'error': None, 'message': 'Test case update'}, status=status.HTTP_200_OK)
    
class get_test_case(ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        test_part_instance = test_part.objects.get(id=request.data['test_part_id'])
        test_case_instances = test_case.objects.filter(test_part=test_part_instance)

        if not test_case_instances:
            return JsonResponse({'error': 'No matching test cases found', 'message': 'failed'}, status=status.HTTP_404_NOT_FOUND)

        test_cases_data = []
        for test_case_instance in test_case_instances:
            variables = variable.objects.filter(test_case=test_case_instance)
            variable_data = variables.values('var', 'input')
            variable_json = json.dumps(list(variable_data))

            test_case_data = {
                'id': test_case_instance.id,
                'output': test_case_instance.output,
                'variables': variable_json
            }
            test_cases_data.append(test_case_data)

        test_part_data = {
            'id': test_part_instance.id,
            'name': test_part_instance.name
        }

        return JsonResponse({
            'error': None,
            'message': 'success',
            'test_part': test_part_data,
            'test_cases': test_cases_data
        }, status=status.HTTP_200_OK)