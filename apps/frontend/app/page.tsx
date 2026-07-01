"use client";

import { useEffect, useState } from "react";
import {
  COURSE_COMPLETIONS_KEY,
  type CourseCompletion,
} from "./courses/CourseTable";
import { storage } from "./utils/localStorage";

const DAYS = ["時限", "月", "火", "水", "木", "金"];

type Course = {
  title: string;
  classroom: string;
};

const CourseComponent = ({ title, classroom }: Course) => {
  return (
    <>
      <span>{title}</span>
      <span>{classroom}</span>
    </>
  );
};

export default function Home() {
  const [courseCompletions, setCourseCompletions] = useState<
    CourseCompletion[]
  >([]);

  useEffect(() => {
    setCourseCompletions(
      storage.get<CourseCompletion[]>(COURSE_COMPLETIONS_KEY, []),
    );
  }, []);

  console.log(courseCompletions);

  return (
    <div>
      <table>
        <thead>
          <tr>
            {DAYS.map((day) => (
              <th scope="col" key={day}>
                {day}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">1限</th>
            <td>{courseCompletions[0].title}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
