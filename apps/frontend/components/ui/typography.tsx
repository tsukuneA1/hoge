import { cn } from '@/lib/utils';

import type * as React from 'react';

type TypographyH1Props = React.HTMLAttributes<HTMLHeadingElement>;

export const TypographyH1 = ({
  className,
  children,
  ...props
}: TypographyH1Props) => {
  return (
    <h1
      className={cn(
        'font-medium text-2xl text-primary leading-[107%] tracking-[10%]',
        className,
      )}
      {...props}
    >
      {children}
    </h1>
  );
};

type TypographyH2Props = React.HTMLAttributes<HTMLHeadingElement>;

export const TypographyH2 = ({
  className,
  children,
  ...props
}: TypographyH2Props) => {
  return (
    <h2
      className={cn(
        'font-medium text-xl text-primary leading-[107%] tracking-[10%]',
        className,
      )}
      {...props}
    >
      {children}
    </h2>
  );
};

type TypographyH3Props = React.HTMLAttributes<HTMLHeadingElement>;

export const TypographyH3 = ({
  className,
  children,
  ...props
}: TypographyH3Props) => {
  return (
    <h3
      className={cn(
        'font-[500] text-primary tracking-wider xl:text-xl',
        className,
      )}
      {...props}
    >
      {children}
    </h3>
  );
};
