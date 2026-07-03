import React from 'react';
import { CheckCircle2, AlertTriangle, FileWarning, PenLine, ArrowDown, ArrowRight, ArrowUp, AlertCircle } from 'lucide-react';

export const labels = [
  {
    value: 'bug',
    label: 'Bug',
  },
  {
    value: 'feature',
    label: 'Feature',
  },
  {
    value: 'documentation',
    label: 'Documentation',
  },
]

export type Severity = 'critical' | 'warning' | 'good' | 'neutral'

export const severityToBadgeVariant: Record<
  Severity,
  'destructive' | 'warning' | 'success' | 'secondary'
> = {
  critical: 'destructive',
  warning: 'warning',
  good: 'success',
  neutral: 'secondary',
}

export const statuses: {
  label: string
  value: string
  icon: React.ComponentType<{ className?: string }>
  severity: Severity
}[] = [
  { label: 'Compliant', value: 'compliant', icon: CheckCircle2, severity: 'good' },
  { label: 'Conditional Hold', value: 'conditional_hold', icon: AlertTriangle, severity: 'warning' },
  { label: 'Incomplete', value: 'incomplete', icon: FileWarning, severity: 'warning' },
  { label: 'Missing Signature', value: 'missing_signature', icon: PenLine, severity: 'critical' },
]

export const priorities = [
  {
    label: 'Low',
    value: 'low' as const,
    icon: ArrowDown,
  },
  {
    label: 'Medium',
    value: 'medium' as const,
    icon: ArrowRight,
  },
  {
    label: 'High',
    value: 'high' as const,
    icon: ArrowUp,
  },
  {
    label: 'Critical',
    value: 'critical' as const,
    icon: AlertCircle,
  },
]
