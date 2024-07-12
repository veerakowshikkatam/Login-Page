def test_user(new_user):
    assert new_user.username == "Koows"
    assert new_user.password == "123435"
    assert new_user.course_id == 4

def test_course(new_course):
    assert new_course.course_name == "Safety and Security"
    assert new_course.course_fees == 40500