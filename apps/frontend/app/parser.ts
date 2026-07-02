import type { RegisteredCourse } from "./courses/CourseTable";

export const DAYS = ["月", "火", "水", "木", "金", "土"] as const;
export const PERIODS = [1, 2, 3, 4, 5, 6, 7] as const;

export type Day = (typeof DAYS)[number];
export type Period = (typeof PERIODS)[number];

export type ParsedSchedule = {
  day: Day | null;
  period: Period | null;
};

export function parseTermDayPeriod(value: string | null): ParsedSchedule {
  if (!value) {
    return { day: null, period: null };
  }

  const normalized = value.normalize("NFKC");

  const dayMatch = normalized.match(/[月火水木金土]/);
  const periodMatch = normalized.match(/([1-7])\s*時限?/);

  const day = dayMatch?.[0] as Day | undefined;
  const period = periodMatch ? Number(periodMatch[1]) : null;

  return {
    day: day ?? null,
    period: isPeriod(period) ? period : null,
  };
}

function isPeriod(value: number | null): value is Period {
  return value !== null && PERIODS.includes(value as Period);
}

export function getScheduledCourses(courses: RegisteredCourse[]) {
  return courses.map((course) => ({
    course,
    schedule: parseTermDayPeriod(course.termDayPeriod),
  }));
}
