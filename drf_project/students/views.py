from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Student
from .serializers import StudentSerializer


class StudentListCreateView(APIView):

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Student created successfully",
                    "student": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentDetailView(APIView):

    def get_student(self, student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return None

    def get(self, request, student_id):
        student = self.get_student(student_id)

        if student is None:
            return Response(
                {"detail": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student)

        return Response(serializer.data)

    def put(self, request, student_id):
        student = self.get_student(student_id)

        if student is None:
            return Response(
                {"detail": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Student updated successfully",
                    "student": serializer.data
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, student_id):
        student = self.get_student(student_id)

        if student is None:
            return Response(
                {"detail": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentSerializer(student)
        student_data = serializer.data

        student.delete()

        return Response(
            {
                "message": "Student deleted successfully",
                "student": student_data
            }
        )