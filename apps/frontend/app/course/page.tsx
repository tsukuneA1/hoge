// app/courses/page.tsx
import { listCourses } from "@/app/utils/api/courses";
import { CourseSearch } from "./CourseSearch";
import { CoursesTable } from "./CourseTable";

const LIMIT = 10;

type PageProps = {
  searchParams: Promise<{
    page?: string | string[];
    limit?: string | string[];
    q?: string | string[];
  }>;
};

function parseIntParam(
  value: string | string[] | undefined,
  defaultValue: number,
): number {
  const raw = Array.isArray(value) ? value[0] : value;
  if (raw == null) return defaultValue;

  const parsed = Number(raw);
  return Number.isInteger(parsed) ? parsed : defaultValue;
}

function parseStringParam(
  value: string | string[] | undefined,
  defaultValue: string | undefined,
): string | undefined {
  const raw = Array.isArray(value) ? value[0] : value;
  if (raw == null) return defaultValue;

  return raw;
}

export default async function CoursePage({ searchParams }: PageProps) {
  const params = await searchParams;

  const page = parseIntParam(params.page, 1);
  const limit = parseIntParam(params.limit, LIMIT);
  const q = parseStringParam(params.q, undefined);
  const offset = (page - 1) * limit;

  const courses = await listCourses({
    academicYear: 2026,
    limit,
    offset,
    q,
  });

  const maxPageNumber = Math.ceil(courses.total / limit);

  return (
    <div className="p-10">
      <CourseSearch />
      <CoursesTable
        data={courses.items}
        pageNumber={page}
        maxPageNumber={maxPageNumber}
      />
    </div>
  );
}
