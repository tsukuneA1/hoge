// app/courses/page.tsx
import { listCourses } from "@/app/utils/api/courses";
import { CourseSearch } from "./CourseSearch";
import { CoursesTable } from "./CourseTable";

const LIMIT = 10;

type PageProps = {
  searchParams: Promise<{
    offset?: string | string[];
    limit?: string | string[];
    q?: string | string[];
    faculty?: string | string[];
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

  const limit = parseIntParam(params.limit, LIMIT);
  const q = parseStringParam(params.q, undefined);
  const offset = parseIntParam(params.offset, 0);
  const faculty = parseStringParam(params.faculty, undefined);

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
