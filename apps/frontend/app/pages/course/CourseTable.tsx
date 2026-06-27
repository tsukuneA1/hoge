// app/courses/CoursesTable.tsx
"use client";

import { BaseTable } from "@/app/components/BaseTable";
import { ColumnDef } from "@tanstack/react-table";
import { useRouter, useSearchParams } from "next/navigation";

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
  pageNumber: number;
  maxPageNumber: number;
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

export function CoursesTable({ data, pageNumber, maxPageNumber }: Props) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const moveToPage = (nextPage: number) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set("page", String(nextPage));

    router.push(`course?${params.toString()}`);
  };

  return (
    <BaseTable
      columns={columns}
      data={data}
      pageNumber={pageNumber}
      maxPageNumber={maxPageNumber}
      onClickNextPage={() => moveToPage(pageNumber + 1)}
      onClickPreviousPage={() => moveToPage(pageNumber - 1)}
      onRowClick={(row) => {
        console.log(row);
      }}
      emptyMessage="hogehoge"
      emptyIcon
    />
  );
}
