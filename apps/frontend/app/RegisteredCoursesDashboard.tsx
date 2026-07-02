"use client";

import { useEffect, useState } from "react";
import {
  REGISTERED_COURSES__KEY,
  type RegisteredCourse,
} from "./courses/CourseTable";
import { Timetable } from "./timetable";
import { storage } from "./utils/localStorage";

export const RegisteredCoursesDashboard = () => {
  const [courses, setCourses] = useState<RegisteredCourse[] | null>(null);

  useEffect(() => {
    setCourses(storage.get<RegisteredCourse[]>(REGISTERED_COURSES__KEY, []));
  }, []);

  if (courses === null) {
    return (
      <div>
        <h1 className="text-2xl font-bold">登録した授業</h1>
        <p className="mt-4 text-sm text-muted-foreground">読み込み中...</p>
      </div>
    );
  }

  return (
    <div>
      <Timetable courses={courses} />
      {/* <UnscheduledCourseList courses={courses} /> */}
    </div>
  );
};
