// app/courses/page.tsx
import { listCourses } from "@/app/utils/api/courses";
import { CourseSearch } from "./CourseSearch";
import { CoursesTable } from "./CourseTable";
import { courseSeachParamsCache } from "./searchParams";

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function CoursePage({ searchParams }: PageProps) {
  const { q, limit, offset, faculty } =
    await courseSeachParamsCache.parse(searchParams);

  const courses = await listCourses({
    academicYear: 2026,
    limit,
    offset,
    q,
    faculty,
  });

  return (
    <div className="p-10 flex flex-col gap-2">
      <CourseSearch />
      <CoursesTable
        data={courses.items}
        limit={limit}
        offset={offset}
        total={courses.total}
      />
    </div>
  );
}
