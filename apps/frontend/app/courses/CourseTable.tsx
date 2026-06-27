// app/courses/CoursesTable.tsx
"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { useRouter, useSearchParams } from "next/navigation";
import { BaseTable } from "@/app/components/BaseTable";

type CourseListItem = {
  pkey: string;
  academic_year: number;
  faculty: string;
  title: string;
  instructor: string;
  term_day_period: string;
  category: string | null;
  eligible_year: string | null;
  credits: number;
  campus: string | null;
  course_key: string | null;
  class_code: string | null;
  language: string | null;
  delivery_mode: string | null;
  field_large: string | null;
  field_middle: string | null;
  field_small: string | null;
  level: string | null;
  class_format: string | null;
};

type Props = {
  data: CourseListItem[];
  limit: number;
  offset: number;
  total: number;
};

const columns: ColumnDef<CourseListItem>[] = [
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
];

export function CoursesTable({ data, limit, offset, total }: Props) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const moveToPage = (nextOffset: number) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set("offset", String(nextOffset));

    router.push(`courses?${params.toString()}`);
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
        console.log(row);
      }}
      emptyMessage="hogehoge"
      emptyIcon
    />
  );
}
