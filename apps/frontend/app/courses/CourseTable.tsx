// app/courses/CoursesTable.tsx
"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { useRouter } from "next/navigation";
import { useQueryStates } from "nuqs";
import type React from "react";
import { useEffect, useMemo, useState } from "react";
import { BaseTable } from "@/app/components/BaseTable";
import { Input } from "@/components/ui/input";
import type { components } from "../utils/api/generated/schema";
import { storage } from "../utils/localStorage";
import { courseSearchParams } from "./searchParams";

type CourseListItem = components["schemas"]["CourseListItem"];

type Props = {
  data: CourseListItem[];
  total: number;
};

export type CourseCompletion = {
  pkey: string;
  title: string;
  classroom: string | null;
  termDayPeriod: string | null;
};

export const COURSE_COMPLETIONS_KEY = "course_completions";

export function CoursesTable({ data, total }: Props) {
  const router = useRouter();
  const [{ limit, offset }, setParams] = useQueryStates(courseSearchParams);

  const [courseCompletions, setCourseCompletions] = useState<
    CourseCompletion[]
  >([]);

  useEffect(() => {
    setCourseCompletions(
      storage.get<CourseCompletion[]>(COURSE_COMPLETIONS_KEY, []),
    );
  }, []);

  const columns = useMemo<ColumnDef<CourseListItem>[]>(
    () => [
      {
        accessorKey: "title",
        header: () => (
          <div className="flex flex-row items-center gap-1.5">
            <div>授業名</div>
          </div>
        ),
        meta: {
          headerClass: "flex-1",
          class: "flex-1",
        },
      },
      {
        id: "faculty",
        header: () => (
          <div className="flex flex-row items-center gap-1.5">
            <div>開講学部</div>
          </div>
        ),
        cell: ({ row }) => {
          if (row.original.faculty.length === 0) {
            return "なし";
          }

          return (
            <div className="flex flex-row items-center gap-2">
              {row.original.faculty}
            </div>
          );
        },
        meta: {
          headerClass: "flex-1",
          class: "flex-1",
        },
      },
      {
        id: "term_day_period",
        header: () => (
          <div className="flex flex-row items-center gap-1.5">
            <div>曜日時限</div>
          </div>
        ),
        cell: ({ row }) => {
          if (row.original.term_day_period.length === 0) {
            return "なし";
          }

          return (
            <div className="flex flex-row items-center gap-2">
              {row.original.term_day_period}
            </div>
          );
        },
        meta: {
          headerClass: "flex-1",
          class: "flex-1",
        },
      },
      {
        id: "course_completion",
        header: () => (
          <div className="flex flex-row items-center gap-1.5">
            <div>授業を追加</div>
          </div>
        ),
        cell: ({ row }) => {
          const checked = courseCompletions.some(
            (courseCompletion) => courseCompletion.pkey === row.original.pkey,
          );

          const handleCheckboxChange = (
            e: React.ChangeEvent<HTMLInputElement>,
          ) => {
            e.stopPropagation();

            const next = e.target.checked
              ? [
                  ...courseCompletions,
                  {
                    pkey: row.original.pkey,
                    title: row.original.title,
                    classroom: row.original.classroom,
                    termDayPeriod: row.original.term_day_period,
                  },
                ]
              : courseCompletions.filter(
                  (courseCompletion) =>
                    courseCompletion.pkey !== row.original.pkey,
                );

            setCourseCompletions(next);
            storage.set<CourseCompletion[]>(COURSE_COMPLETIONS_KEY, next);
          };

          return (
            <Input
              type="checkbox"
              checked={checked}
              onChange={handleCheckboxChange}
              onClick={(e) => e.stopPropagation()}
            />
          );
        },
      },
    ],
    [courseCompletions],
  );

  const moveToPage = (nextOffset: number) => {
    void setParams(
      {
        offset: nextOffset,
      },
      {
        history: "replace",
        shallow: false,
      },
    );
  };

  return (
    <BaseTable
      columns={columns}
      data={data}
      limit={limit}
      offset={offset}
      total={total}
      onClickNextPage={() => moveToPage(offset + limit)}
      onClickPreviousPage={() => moveToPage(offset - limit)}
      onRowClick={(row) => {
        router.push(`/courses/${row.pkey}`);
      }}
      emptyMessage="hogehoge"
      emptyIcon
    />
  );
}
