"use client";

import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  type RowData,
  useReactTable,
} from "@tanstack/react-table";
import classNames from "classnames";
import { ChevronLeft, ChevronRight } from "lucide-react";

type Props<T> = {
  columns: ColumnDef<T>[];
  data: T[];
  limit: number;
  offset: number;
  total: number;
  onClickNextPage: () => void;
  onClickPreviousPage: () => void;
  emptyMessage: string;
  emptyIcon: React.ReactNode;
  onRowClick?: (row: T) => void;
};

declare module "@tanstack/react-table" {
  interface ColumnMeta<TData extends RowData, TValue> {
    headerClass?: string;
    class?: string;
  }
}

export function BaseTable<T>(props: Props<T>) {
  const table = useReactTable<T>({
    data: props.data,
    columns: props.columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const previousDisabled = props.offset === 0;
  const nextDisabled = props.offset + props.limit >= props.total;

  return (
    <div className="flex flex-col gap-1 items-start self-stretch">
      <div className="flex flex-col items-start self-stretch rounded-t-[16px] border-solid border border-input bg-surface-primary">
        {table.getHeaderGroups().map((headerGroup) => (
          <div
            key={headerGroup.id}
            className="flex h-12 px-6 items-center gap-6 self-stretch text-primary"
          >
            {headerGroup.headers.map((header) => (
              <div
                key={header.id}
                className={classNames(
                  "text-left text-sm font-normal leading-[1.4]",

                  header.column.columnDef.meta?.headerClass,
                )}
              >
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.header,
                      header.getContext(),
                    )}
              </div>
            ))}
          </div>
        ))}
      </div>
      {props.data.length === 0 ? (
        <div className="flex flex-col gap-3 items-center justify-center py-9 mx-auto body-m text-tertiary">
          {props.emptyIcon}
          {props.emptyMessage}
        </div>
      ) : (
        <div className="px-5 flex flex-col items-start self-stretch rounded-b-[16px] border-solid border-1 border-border bg-surface-primary">
          {table.getRowModel().rows.map((row, index) => (
            <button
              key={row.id}
              type="button"
              className={`flex flex-row px-6 py-4 gap-6 items-center self-stretch body-s text-primary w-full text-left border-solid border-b border-border
              ${props.onRowClick ? "cursor-pointer" : ""}`}
              onClick={() => props.onRowClick?.(row.original)}
            >
              {row.getVisibleCells().map((cell) => (
                <div
                  key={cell.id}
                  className={classNames(
                    "whitespace-nowrap text-ellipsis overflow-hidden text-sm text-primary",

                    cell.column.columnDef.meta?.class,
                  )}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </div>
              ))}
            </button>
          ))}
          <div className="flex h-14 px-6 justify-end items-center self-stretch border-b-solid border-b border-input">
            <div className="flex justify-center items-center gap-4">
              <div className="text-caption-s text-primary">
                {props.offset + 1} -{" "}
                {Math.min(props.offset + props.limit, props.total)} of{" "}
                {props.total}
              </div>
              <div className="flex justify-center items-center gap-2">
                <button
                  type="button"
                  className={classNames(
                    previousDisabled
                      ? "text-tertiary"
                      : "text-primary cursor-pointer",
                  )}
                  onClick={props.onClickPreviousPage}
                  disabled={previousDisabled}
                >
                  {previousDisabled ? (
                    <div className="inline-flex items-center justify-center rounded-full bg-background p-2">
                      <ChevronLeft className="h-5 w-5 text-chart-2" />
                    </div>
                  ) : (
                    <div className="inline-flex items-center justify-center rounded-full bg-chart-1 p-2">
                      <ChevronLeft className="h-5 w-5 text-primary" />
                    </div>
                  )}
                </button>
                <button
                  type="button"
                  className={classNames(
                    nextDisabled
                      ? "text-tertiary"
                      : "text-primary cursor-pointer",
                  )}
                  onClick={props.onClickNextPage}
                  disabled={nextDisabled}
                >
                  {nextDisabled ? (
                    <div className="inline-flex items-center justify-center rounded-full bg-background p-2">
                      <ChevronRight className="h-5 w-5 text-chart-2" />
                    </div>
                  ) : (
                    <div className="inline-flex items-center justify-center rounded-full bg-chart-1 p-2">
                      <ChevronRight className="h-5 w-5 text-primary" />
                    </div>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
