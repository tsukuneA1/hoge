import Link from "next/link";
import type { RegisteredCourse } from "./courses/CourseTable";
import { DAYS, PERIODS, parseTermDayPeriod } from "./parser";

type Props = {
  courses: RegisteredCourse[];
};

export const Timetable = ({ courses }: Props) => {
  const scheduledCourses = courses.filter((course) => {
    const schedule = parseTermDayPeriod(course.termDayPeriod);
    return schedule.day !== null && schedule.period !== null;
  });

  const getCoursesAt = (day: string, period: number) => {
    return scheduledCourses.filter((course) => {
      const schedule = parseTermDayPeriod(course.termDayPeriod);
      return schedule.day === day && schedule.period === period;
    });
  };

  return (
    <div className="mt-4 overflow-x-auto rounded-lg border">
      <table className="w-full min-w-[760px] border-collapse text-sm">
        <thead>
          <tr className="border-b bg-muted/50">
            <th className="w-16 px-3 py-2 text-left font-medium">時限</th>
            {DAYS.map((day) => (
              <th key={day} className="px-3 py-2 text-left font-medium">
                {day}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {PERIODS.map((period) => (
            <tr key={period} className="border-b last:border-b-0">
              <th className="px-3 py-3 text-left align-top font-medium">
                {period}
              </th>

              {DAYS.map((day) => {
                const coursesAtCell = getCoursesAt(day, period);

                return (
                  <td key={day} className="min-h-24 px-3 py-3 align-top">
                    <div className="space-y-2">
                      {coursesAtCell.map((course) => (
                        <CourseCell key={course.pkey} course={course} />
                      ))}
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

function CourseCell({ course }: { course: RegisteredCourse }) {
  return (
    <Link
      href={`/courses/${encodeURIComponent(course.pkey)}`}
      className="block rounded-md border bg-background p-2 hover:bg-muted"
    >
      <div className="line-clamp-2 font-medium">{course.title}</div>
      {course.classroom ? (
        <div className="mt-1 text-xs text-muted-foreground">
          {course.classroom}
        </div>
      ) : null}
    </Link>
  );
}
